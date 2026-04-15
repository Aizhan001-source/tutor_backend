from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from data_access.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    avatar_url = Column(String(500))

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="users")

    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active")

    tutor_profile = relationship(
        "TutorProfile",
        back_populates="user",
        uselist=False
    )

    student_profile = relationship(
    "StudentProfile",
    back_populates="user",
    uselist=False
)
    
    payments = relationship("Payment", back_populates="user")