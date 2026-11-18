from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application_model import Application
from app.applications import ApplicationResponse
from app.auth import get_active_session, unauthorized
from app.database import get_db
from app.models import LoginSession, User

router = APIRouter(prefix="/reviews", tags=["Reviews"])


def get_reviewer(
    login_session: LoginSession = Depends(get_active_session),
    db: Session = Depends(get_db),
) -> User:
    user = db.get(User, login_session.user_id)
    if user is None:
        raise unauthorized("Your session is invalid or expired.")
    if user.role != "reviewer":
        raise HTTPException(status_code=403, detail="Reviewer access required.")
    return user


@router.get("/queue", response_model=list[ApplicationResponse])
def list_review_queue(
    reviewer: User = Depends(get_reviewer),
    db: Session = Depends(get_db),
):
    query = (
        select(Application)
        .where(Application.status == "submitted")
        .order_by(Application.id)
    )
    return db.scalars(query).all()