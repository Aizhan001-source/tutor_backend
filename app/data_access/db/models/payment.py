import uuid
from enum import Enum 
from sqlalchemy import ( 
    Column, String, ForeignKey, 
    Numeric, TIMESTAMP, Enum as SqlEnum, CheckConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from data_access.db.base import Base


class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False, index=True)

    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="KZT", nullable=False)

    status = Column(SqlEnum(PaymentStatus), default=PaymentStatus.pending, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    booking = relationship("Booking", back_populates="payments")