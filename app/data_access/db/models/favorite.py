import uuid
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (Column, ForeignKey, TIMESTAMP, UniqueConstraint)
from sqlalchemy.orm import relationship

from data_access.db.base import Base



class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    __table_args__ = (
        UniqueConstraint("user_id", "tutor_id", name="unique_favorite"),
    )

    user = relationship("User", foreign_keys=[user_id], back_populates="favorite_tutors")
    tutor = relationship("User", foreign_keys=[tutor_id], back_populates="favorited_by")

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),onupdate=func.now())
