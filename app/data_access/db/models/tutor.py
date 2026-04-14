import uuid
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, String, TIMESTAMP, ForeignKey,
    Text, Integer, Numeric, CheckConstraint, Enum as SqlEnum)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from data_access.db.base import Base

class LessonFormat(str, PyEnum):
    online = "online"
    offline = "offline"
    hybrid = "hybrid"

class Tutor(Base):
    __tablename__ = "tutors"
    __table_args__ = (
        CheckConstraint("average_rating >= 0 AND average_rating <= 5"),
        CheckConstraint("price_per_hour > 0"),
        CheckConstraint("experience_years >= 0"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False, index=True)

    bio = Column(Text)
    experience_years = Column(Integer)
    education = Column(Text)

    price_per_hour = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="KZT")

    format = Column(SqlEnum(LessonFormat, name="lesson_format"), nullable=False)
    city = Column(String(150))

    average_rating = Column(Numeric(3, 2), default=0)
    total_reviews = Column(Integer, default=0)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),onupdate=func.now(),server_onupdate=func.now())

    user = relationship("User", back_populates="tutor_profile")
    subject = relationship("Subject", back_populates="tutors")