from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "concelled"

class BookingCreate(BaseModel):
    tutor_is: int
    start_time: datetime
    end_time: datetime

class BookingRead(BaseModel):
    id: int
    student_id: int
    tutor_id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus

    class Config:
        from_attributes = True