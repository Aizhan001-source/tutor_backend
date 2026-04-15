from sqlalchemy import Column, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from data_access.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)

    status = Column(
        Enum("pending", "paid", "failed", name="payment_status"),
        default="pending",
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")
    session = relationship("Session", back_populates="payments")