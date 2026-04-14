import uuid
from sqlalchemy.sql import func 
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ( Column, String, Boolean, ForeignKey, TIMESTAMP)

from data_access.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    avatar_url = Column(String(100))

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    role = relationship("Role", back_populates="users")
    admin = relationship("Admin", back_populates="user", uselist=False)
    
    # связь между User и Tutor (1 к 1).
    tutor_profile = relationship("Tutor", back_populates="user", uselist=False)

    student_bookings = relationship("Booking",foreign_keys="Booking.student_id",back_populates="student")
    tutor_bookings = relationship("Booking",foreign_keys="Booking.tutor_id",back_populates="tutor")

    # for reviews
    given_reviews = relationship("Review", foreign_keys="Review.student_id", back_populates="student")
    received_reviews = relationship("Review", foreign_keys="Review.tutor_id", back_populates="tutor")

    # for favorite
    favorite_tutors = relationship("Favorite", foreign_keys="Favorite.user_id", back_populates="user")
    favorited_by = relationship("Favorite", foreign_keys="Favorite.tutor_id", back_populates="tutor")
    
    # for message
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    