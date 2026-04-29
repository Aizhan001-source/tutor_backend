from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String)

from data_access.db.base import Base


class Education(Base):
    __tablename__ = "educations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True)

    tutors = relationship("Tutor", back_populates="education")
