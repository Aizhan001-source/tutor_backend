from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PaymentCreate(BaseModel):
    booking_id: UUID
    amount: float
    currency: str = "KZT"


class PaymentRead(BaseModel):
    id: UUID
    booking_id: UUID
    amount: float
    currency: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}