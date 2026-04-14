from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PaymentCreate(BaseModel):
    booking_id: UUID
    amount: float
    method: str  # "card", "cash", "online"

class PaymentRead(BaseModel):
    id: UUID
    booking_id: UUID
    student_id: UUID
    amount: float
    method: str
    status: str  # "pending", "paid", "failed"
    created_at: datetime

    model_config = {"from_attributes": True}