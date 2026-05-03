from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from sqlalchemy import (Column, TIMESTAMP, ForeignKey)

from data_access.db.base import Base


class CourseStudent(Base):
    __tablename__ = "course_students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())