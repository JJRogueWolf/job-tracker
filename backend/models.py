from datetime import date
from datetime import datetime, timezone
from sqlalchemy import DateTime
from uuid import UUID, uuid4

from sqlalchemy import Date, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class JobDB(Base):
    __tablename__ = "jobs"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4
    )

    company: Mapped[str] = mapped_column(String(200))
    position: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(30))
    appliedDate: Mapped[date] = mapped_column(Date)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )