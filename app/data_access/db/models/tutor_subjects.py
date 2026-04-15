from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from data_access.db.base import Base


class TutorSubject(Base):
    __tablename__ = "tutor_subjects"

    tutor_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tutor_profiles.id"),
        primary_key=True
    )

    subject_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id"),
        primary_key=True
    )

    __table_args__ = (
        UniqueConstraint("tutor_profile_id", "subject_id", name="unique_tutor_subject"),
    )