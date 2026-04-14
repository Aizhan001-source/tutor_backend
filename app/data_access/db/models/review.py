import uuid
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (Column, String, ForeignKey, Integer, TIMESTAMP)
from sqlalchemy.orm import relationship

from data_access.db.base import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"))

    rating = Column(Integer, nullable=False)
    comment = Column(String(1000))

    created_at = Column(TIMESTAMP, server_default=func.now())

    # связи
    student = relationship("User", foreign_keys=[student_id])
    tutor = relationship("User", foreign_keys=[tutor_id])
    booking = relationship("Bookings")

