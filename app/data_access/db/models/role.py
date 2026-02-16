from sqlalchemy import (
    Column, String, Boolean, Integer, Text,
    ForeignKey, Numeric, TIMESTAMP
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid
from sqlalchemy.sql import func
from data_access.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    users = relationship("User", back_populates="role")
