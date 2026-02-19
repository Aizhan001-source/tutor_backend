from sqlalchemy import (
    Column, String, Boolean,
    ForeignKey, TIMESTAMP
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.sql import func

from data_access.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20))
    first_name = Column(String(100))
    last_name = Column(String(100))
    avatar_url = Column(String(500))

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    role = relationship("Role", back_populates="users")
    tutor_profile = relationship("Tutor", back_populates="user", uselist=False)
