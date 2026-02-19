from sqlalchemy import (
    Column, String, Boolean, Integer, Text,
    ForeignKey, Numeric, TIMESTAMP
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid
from sqlalchemy.sql import func

from data_access.db.base import Base

class Tutor(Base):
    __tablename__ = "tutors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)

    bio = Column(Text)
    experience_years = Column(Integer)
    education = Column(Text)

    price_per_hour = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="KZT")

    format = Column(String(20))  # online / offline / both
    city = Column(String(150))

    average_rating = Column(Numeric(3, 2), default=0)
    total_reviews = Column(Integer, default=0)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="tutor_profile")
