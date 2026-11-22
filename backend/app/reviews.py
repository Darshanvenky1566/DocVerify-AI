from typing import Literal
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application_model import Application
from app.applications import ApplicationResponse
from app.auth import get_active_session, unauthorized
from app.database import get_db
from app.document_model import Document
from app.documents import DocumentResponse
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


@router.get(
    "/{application_id}/documents",
    response_model=list[DocumentResponse],
)
def list_review_documents(
    application_id: int,
    reviewer: User = Depends(get_reviewer),
    db: Session = Depends(get_db),
):
    application = db.get(Application, application_id)
    if application is None or application.status != "submitted":
        raise HTTPException(status_code=404, detail="Application not found.")

    query = (
        select(Document)
        .where(Document.application_id == application.id)
        .order_by(Document.id)
    )
    return db.scalars(query).all()


@router.get("/{application_id}/documents/{document_id}/download")
def download_review_document(
    application_id: int,
    document_id: int,
    reviewer: User = Depends(get_reviewer),
    db: Session = Depends(get_db),
):
    document = db.scalar(
        select(Document)
        .join(Application, Application.id == Document.application_id)
        .where(
            Document.id == document_id,
            Application.id == application_id,
            Application.status == "submitted",
        )
    )
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    filename = quote(document.filename, safe="")
    fallback = "".join(
        char if char.isascii() and (char.isalnum() or char in "._-") else "_"
        for char in document.filename
    )
    return Response(
        content=document.content,
        media_type=document.content_type,
        headers={
            "Content-Disposition": (
                f'attachment; filename="{fallback}"; '
                f"filename*=UTF-8''{filename}"
            )
        },
    )