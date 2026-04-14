import uuid
from enum import Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Enum as SqlEnum

from data_access.db.base import Base

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    status = Column(SqlEnum(BookingStatus, name="booking_status"),default=BookingStatus.pending)
    cancel_reason = Column(String(255), nullable=True)
    
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # relationships
    student = relationship("User",foreign_keys=[student_id],back_populates="student_bookings")
    tutor = relationship("User",foreign_keys=[tutor_id],back_populates="tutor_bookings")

    payments = relationship("Payment", back_populates="booking")

    review = relationship("Review", back_populates="booking", uselist=False)