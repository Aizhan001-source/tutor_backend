from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal


class TutorCreate(BaseModel):
    bio: str | None = None
    experience_years: int | None = None
    education: str | None = None
    price_per_hour: Decimal
    currency: str = "KZT"
    format: str | None = None
    city: str | None = None


class TutorUpdate(BaseModel):
    bio: str | None = None
    experience_years: int | None = None
    education: str | None = None
    price_per_hour: Decimal | None = None
    format: str | None = None
    city: str | None = None


class TutorRead(BaseModel):
    id: UUID
    user_id: UUID
    bio: str | None
    experience_years: int | None
    education: str | None
    price_per_hour: Decimal
    currency: str
    format: str | None
    city: str | None
    average_rating: Decimal
    total_reviews: int

    class Config:
        from_attributes = True