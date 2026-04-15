from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime

from data_access.db.base import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)



    tutors = relationship(
    "TutorProfile",
    secondary="tutor_subjects",
    back_populates="subjects"
)
    
    students = relationship(
    "StudentProfile",
    secondary="student_subjects",
    back_populates="subjects"
)