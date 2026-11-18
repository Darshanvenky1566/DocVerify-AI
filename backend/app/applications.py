from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application_model import Application
from app.auth import get_active_session, unauthorized
from app.database import get_db
from app.models import LoginSession, User

router = APIRouter(prefix="/applications", tags=["Applications"])


class ApplicationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=150)


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: str
    created_at: datetime


def get_applicant(
    login_session: LoginSession = Depends(get_active_session),
    db: Session = Depends(get_db),
) -> User:
    user = db.get(User, login_session.user_id)
    if user is None:
        raise unauthorized("Your session is invalid or expired.")
    if user.role != "applicant":
        raise HTTPException(status_code=403, detail="Applicant access required.")
    return user


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    data: ApplicationCreate,
    applicant: User = Depends(get_applicant),
    db: Session = Depends(get_db),
):
    title = data.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Enter an application title.")

    application = Application(title=title, applicant_id=applicant.id)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("", response_model=list[ApplicationResponse])
def list_applications(
    applicant: User = Depends(get_applicant),
    db: Session = Depends(get_db),
):
    query = (
        select(Application)
        .where(Application.applicant_id == applicant.id)
        .order_by(Application.id.desc())
    )
    return db.scalars(query).all()