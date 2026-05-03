from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel
from uuid import UUID
from api.users.user_schemas import UserRead


class EducationRead(BaseModel):
    id: UUID
    name: str


class TutorRead(BaseModel):
    id: UUID
    bio: Optional[str]
    experience_years: int
    education: EducationRead
    price_per_hour: Optional[Decimal]
    currency: str
    average_rating: Decimal
    total_reviews: int
    user: UserRead

    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True} 