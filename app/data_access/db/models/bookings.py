from datetime import datetime
from enum import Enum

from sqlalchemy import String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_access.db.base import Base

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)   
    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )
    tutor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )
    start_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[BookingStatus] = mapped_column(
        SqlEnum(BookingStatus),
        default=BookingStatus.pending,
        index=True
    )
    cancel_reason: Mapped[str | None ] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # relationships (очень желательно)
    student = relationship("User", foreign_keys=[student_id])
    tutor = relationship("User", foreign_keys=[tutor_id])