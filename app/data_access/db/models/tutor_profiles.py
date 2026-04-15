from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Float, CheckConstraint, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from data_access.db.base import Base


class TutorProfile(Base):
    __tablename__ = "tutor_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    headline = Column(String(255))
    bio = Column(String)

    experience_years = Column(Integer, default=0)
    hourly_rate = Column(Numeric(10, 2))

    rating_avg = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)

    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="tutor_profile")

    __table_args__ = (
        CheckConstraint("experience_years >= 0", name="check_experience"),
    )

    subjects = relationship(
    "Subject",
    secondary="tutor_subjects",
    back_populates="tutors"
)