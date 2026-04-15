from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from data_access.db.base import Base


class StudentSubject(Base):
    __tablename__ = "student_subjects"

    student_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("student_profiles.id"),
        primary_key=True
    )

    subject_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id"),
        primary_key=True
    )

    __table_args__ = (
        UniqueConstraint("student_profile_id", "subject_id", name="unique_student_subject"),
    )