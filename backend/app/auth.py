from datetime import datetime, timedelta, timezone
from hashlib import sha256
from secrets import token_urlsafe

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import LoginSession, User
from app.schemas import TokenResponse, UserLogin, UserRegister, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
password_hasher = PasswordHash.recommended()
bearer = HTTPBearer(auto_error=False)
session_seconds = 3600
dummy_password_hash = password_hasher.hash(token_urlsafe(32))


def hash_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def unauthorized(message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_active_session(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> LoginSession:
    if credentials is None:
        raise unauthorized("Sign in to continue.")

    login_session = db.scalar(
        select(LoginSession).where(
            LoginSession.token_hash == hash_token(credentials.credentials),
            LoginSession.expires_at > datetime.now(timezone.utc),
        )
    )
    if login_session is None:
        raise unauthorized("Your session is invalid or expired.")

    return login_session


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(data: UserRegister, db: Session = Depends(get_db)):
    user = User(
        email=str(data.email).lower(),
        password_hash=password_hasher.hash(data.password),
        role="applicant",
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists.",
        ) from None

    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(
        select(User).where(User.email == str(data.email).lower())
    )
    stored_hash = user.password_hash if user is not None else dummy_password_hash
    password_valid = password_hasher.verify(data.password, stored_hash)

    if user is None or not password_valid:
        raise unauthorized("Invalid email or password.")

    token = token_urlsafe(32)
    db.add(
        LoginSession(
            user_id=user.id,
            token_hash=hash_token(token),
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=session_seconds),
        )
    )
    db.commit()

    response.headers["Cache-Control"] = "no-store"
    return TokenResponse(access_token=token, expires_in=session_seconds)


@router.get("/me", response_model=UserResponse)
def read_profile(
    login_session: LoginSession = Depends(get_active_session),
    db: Session = Depends(get_db),
):
    user = db.get(User, login_session.user_id)
    if user is None:
        raise unauthorized("Your session is invalid or expired.")
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    login_session: LoginSession = Depends(get_active_session),
    db: Session = Depends(get_db),
):
    db.delete(login_session)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/admin/users", response_model=list[UserResponse])
def list_users(
    login_session: LoginSession = Depends(get_active_session),
    db: Session = Depends(get_db),
):
    current_user = db.get(User, login_session.user_id)
    if current_user is None:
        raise unauthorized("Your session is invalid or expired.")

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required.",
        )

    return db.scalars(select(User).order_by(User.id).limit(100)).all()