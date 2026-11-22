from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, LargeBinary, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.application_model import Application
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey(Application.id, ondelete="CASCADE"),
        index=True,
    )
    filename: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(100))
    document_type: Mapped[str] = mapped_column(
        String(50), default="supporting", server_default="supporting"
    )
    notes: Mapped[str] = mapped_column(
        String(2000), default="", server_default=""
    )
    content: Mapped[bytes] = mapped_column(LargeBinary, deferred=True)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
