from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., ge=0)


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)


class CourseRead(CourseBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True