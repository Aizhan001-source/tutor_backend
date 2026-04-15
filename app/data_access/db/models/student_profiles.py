from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from data_access.db.base import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    level = Column(String, nullable=False)  # beginner / intermediate / advanced

    learning_goals = Column(JSONB)  # или Text, но JSONB лучше
    bio = Column(String)

    timezone = Column(String)
    preferred_language = Column(String)

    total_sessions = Column(Integer, default=0)
    completed_sessions = Column(Integer, default=0)
    total_spent_hours = Column(Integer, default=0)

    last_session_at = Column(DateTime)

    user = relationship("User", back_populates="student_profile")


    subjects = relationship(
    "Subject",
    secondary="student_subjects",
    back_populates="students"
)