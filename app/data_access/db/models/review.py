from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from sqlalchemy import (Column, TIMESTAMP, Integer, ForeignKey, Text, UniqueConstraint)

from data_access.db.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)

    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="unique_review"),
    )

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    student = relationship("Student")
    course = relationship("Course")
    