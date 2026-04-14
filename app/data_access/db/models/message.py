import uuid
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
<<<<<<< HEAD
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
=======
from sqlalchemy import (Column, ForeignKey, String, TIMESTAMP, Boolean)
from sqlalchemy.orm import relationship

>>>>>>> origin/lili
from data_access.db.base import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
<<<<<<< HEAD
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    content = Column(String(2000), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
=======

    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    content = Column(String(2000), nullable=False)

    is_read = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, server_default=func.now())

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates=[receiver_id])
    
>>>>>>> origin/lili
