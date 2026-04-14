from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class ReviewCreate(BaseModel):
    student_id: UUID
    tutor_id: UUID
    booking_id: UUID
    raiting: int
    comment: str


class ReviewRead(BaseModel):
    id: UUID
    student_id: UUID
    tutor_id: UUID
    booking_id: UUID
    rating: int
    comment: str

    model_config = {"from_attributes": True}


class ReviewUpdate(BaseModel):
    raiting: Optional[int] = None
    comment: Optional[str] = None


    

