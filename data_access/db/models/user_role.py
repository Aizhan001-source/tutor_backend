from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy import (Column, ForeignKey, UniqueConstraint)

from data_access.db.base import Base


class UserRoles(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
    