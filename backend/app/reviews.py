from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application_model import Application
from app.applications import ApplicationResponse
from app.auth import get_active_session, unauthorized
from app.database import get_db
from app.models import LoginSession, User
from app.review_model import ReviewDecision

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


class ReviewDecisionInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    decision: Literal["approved", "rejected"]
    reason: str = Field(min_length=1, max_length=2000)


@router.post("/{application_id}/decision", response_model=ApplicationResponse)
def decide_application(
    application_id: int,
    data: ReviewDecisionInput,
    reviewer: User = Depends(get_reviewer),
    db: Session = Depends(get_db),
):
    application = db.scalar(
        select(Application)
        .where(Application.id == application_id)
        .with_for_update()
    )
    if application is None or application.status == "draft":
        raise HTTPException(status_code=404, detail="Application not found.")
    if application.status != "submitted":
        raise HTTPException(
            status_code=409,
            detail="Only submitted applications can be reviewed.",
        )

    db.add(
        ReviewDecision(
            application_id=application.id,
            reviewer_id=reviewer.id,
            decision=data.decision,
            reason=data.reason,
        )
    )
    application.status = data.decision
    db.commit()
    db.refresh(application)
    return application