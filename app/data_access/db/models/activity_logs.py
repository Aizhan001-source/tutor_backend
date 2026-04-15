from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from data_access.db.base import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    action = Column(String, nullable=False)  # например: "create_course", "login"

    entity_type = Column(String)  # "course", "user", "session"
    entity_id = Column(UUID(as_uuid=True))  # id объекта

    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 связь
    user = relationship("User")