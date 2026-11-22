import warnings
from datetime import datetime
from io import BytesIO
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from PIL import Image
from pydantic import BaseModel, ConfigDict
from pypdf import PdfReader
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

DocumentType = Literal["supporting", "identity", "qualification"]


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    filename: str
    content_type: str
    document_type: str
    notes: str
    uploaded_at: datetime


def validate_content(content: bytes, extension: str) -> None:
    try:
        if extension == "pdf":
            reader = PdfReader(BytesIO(content), strict=True)
            if reader.is_encrypted:
                raise ValueError("Encrypted PDF")
            if not reader.pages:
                raise ValueError("Empty PDF")
            for page in reader.pages:
                _ = page.mediabox
                stream = page.get_contents()
                if stream is not None:
                    stream.get_data()
        else:
            expected = "PNG" if extension == "png" else "JPEG"
            with warnings.catch_warnings():
                warnings.simplefilter("error", Image.DecompressionBombWarning)
                with Image.open(BytesIO(content)) as image:
                    if image.format != expected:
                        raise ValueError("Image format mismatch")
                    image.verify()
                with Image.open(BytesIO(content)) as image:
                    image.load()
    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=(
                "File is damaged, unreadable, encrypted, or too complex. "
                "Export a new unencrypted PDF, PNG, or JPEG and upload it again."
            ),
        ) from error


@router.post(
    "/{application_id}/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    application_id: int,
    file: Annotated[UploadFile, File()],
    document_type: Annotated[DocumentType, Form()] = "supporting",
    notes: Annotated[str, Form(max_length=2000)] = "",
    applicant: User = Depends(get_applicant),
    db: Session = Depends(get_db),
):
    application = db.scalar(
        select(Application)
        .where(
            Application.id == application_id,
            Application.applicant_id == applicant.id,
        )
        .with_for_update()
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
    if not content:
        raise HTTPException(
            status_code=422,
            detail="File is empty. Upload a readable file.",
        )

    content_type, signature = file_type
    if not content.startswith(signature):
        raise HTTPException(
            status_code=415,
            detail="File content does not match its extension.",
        )

    validate_content(content, extension)

    document = Document(
        application_id=application.id,
        filename=filename,
        content_type=content_type,
        document_type=document_type,
        notes=notes.strip(),
        content=content,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.get(
    "/{application_id}/documents",
    response_model=list[DocumentResponse],
)
def list_documents(
    application_id: int,
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

    query = (
        select(Document)
        .where(Document.application_id == application.id)
        .order_by(Document.id)
    )
    return db.scalars(query).all()

@router.get("/{application_id}/document-checklist")
def document_checklist(
    application_id: int,
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

    document_ids = list(
        db.scalars(
            select(Document.id)
            .where(Document.application_id == application.id)
            .order_by(Document.id)
        ).all()
    )
    return {
        "application_id": application.id,
        "requirements": [
            {
                "description": "Upload at least one supporting document.",
                "minimum_files": 1,
                "uploaded_files": len(document_ids),
                "complete": bool(document_ids),
            }
        ],
        "allowed_document_types": ["supporting", "identity", "qualification"],
        "allowed_extensions": ["pdf", "png", "jpg", "jpeg"],
        "max_file_size_bytes": MAX_FILE_SIZE,
        "document_ids": document_ids,
        "ready_to_submit": application.status == "draft" and bool(document_ids),
    }
