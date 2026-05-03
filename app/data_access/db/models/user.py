from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP

from data_access.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    first_name = Column(String(100))
    last_name = Column(String(100))

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # -------------------
    # RELATIONSHIPS
    # -------------------

    role = relationship("Role", back_populates="users")

    tutor = relationship(
        "Tutor",
        back_populates="user",
        uselist=False
    )

    # 📌 Booking (student side)
    bookings = relationship(
        "Booking",
        foreign_keys="Booking.student_id",
        back_populates="student"
    )

    # 📌 Messages
    sent_messages = relationship(
        "Message",
        foreign_keys="Message.sender_id",
        back_populates="sender",
        cascade="all, delete-orphan"
    )

    received_messages = relationship(
        "Message",
        foreign_keys="Message.receiver_id",
        back_populates="receiver",
        cascade="all, delete-orphan"
    )