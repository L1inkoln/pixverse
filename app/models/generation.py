from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class GenerationTask(Base):
    __tablename__ = "generation_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_type: Mapped[str] = mapped_column(String(20))
    app_bundle_id: Mapped[str] = mapped_column(String(255))
    apphud_user_id: Mapped[str] = mapped_column(String(255))
    prompt: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
