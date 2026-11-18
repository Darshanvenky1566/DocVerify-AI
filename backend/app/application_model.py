from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base, User


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    applicant_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(
        String(20), default="draft", server_default="draft"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )