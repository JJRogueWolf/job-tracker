from datetime import date
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