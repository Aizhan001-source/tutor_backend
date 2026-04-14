from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BookingCreate(BaseModel):
    tutor_id: UUID
    start_time: datetime
    end_time: datetime

class BookingRead(BaseModel):
    id: UUID
    student_id: UUID
    tutor_id: UUID
    start_time: datetime
    end_time: datetime
    status: str

    model_config = {"from_attributes": True}


class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None