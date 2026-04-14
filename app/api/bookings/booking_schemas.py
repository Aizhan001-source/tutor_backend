from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BookingCreate(BaseModel):
    tutor_id: UUID
    start_time: datetime
    end_time: datetime
    subject: str
    notes: Optional[str] = None

class BookingRead(BaseModel):
    id: UUID
    student_id: UUID
    tutor_id: UUID
    start_time: datetime
    end_time: datetime
    subject: str
    notes: Optional[str]
    status: str  # "pending", "confirmed", "canceled"

    model_config = {"from_attributes": True}


class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    subject: Optional[str] = None
    notes: Optional[str] = None