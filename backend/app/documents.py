from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application_model import Application
from app.applications import get_applicant
from app.database import get_db
from app.document_model import Document
from app.models import User

router = APIRouter(prefix="/applications", tags=["Documents"])

MAX_FILE_SIZE = 10 * 1024 * 1024
FILE_TYPES = {
    "pdf": ("application/pdf", b"%PDF-"),
    "png": ("image/png", b"\x89PNG\r\n\x1a\n"),
    "jpg": ("image/jpeg", b"\xff\xd8\xff"),
    "jpeg": ("image/jpeg", b"\xff\xd8\xff"),
}


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    filename: str
    content_type: str
    uploaded_at: datetime


@router.post(
    "/{application_id}/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    application_id: int,
    file: UploadFile = File(...),
    applicant: User = Depends(get_applicant),
    db: Session = Depends(get_db),
):
    application = db.scalar(
        select(Application).where(
            Application.id == application_id,
            Application.applicant_id == applicant.id,
        )
    )
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found.")
    if application.status != "draft":
        raise HTTPException(status_code=409, detail="Only drafts accept uploads.")

    filename = (file.filename or "").replace("\\", "/").rsplit("/", 1)[-1].strip()
    if not filename or len(filename) > 255 or "\x00" in filename:
        raise HTTPException(status_code=422, detail="Enter a valid filename.")

    extension = filename.rpartition(".")[2].lower()
    file_type = FILE_TYPES.get(extension)
    if file_type is None:
        raise HTTPException(status_code=415, detail="Use a PDF, PNG, or JPEG file.")

    content = file.file.read(MAX_FILE_SIZE + 1)
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File exceeds the 10 MiB limit.")

    content_type, signature = file_type
    if not content.startswith(signature):
        raise HTTPException(status_code=415, detail="File content does not match its extension.")

    document = Document(
        application_id=application.id,
        filename=filename,
        content_type=content_type,
        content=content,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document