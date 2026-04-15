from typing import Optional, List
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime



class RoleRead(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}



class TutorProfileRead(BaseModel):
    id: UUID
    user_id: UUID

    headline: Optional[str] = None
    bio: Optional[str] = None

    experience_years: int
    hourly_rate: float

    rating_avg: float
    total_reviews: int

    is_verified: bool

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class TutorUserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    avatar_url: Optional[str] = None

    role: Optional[RoleRead] = None
    tutor_profile: Optional[TutorProfileRead] = None

    model_config = {"from_attributes": True}

class TutorListResponse(BaseModel):
    items: List[TutorUserRead]

    total: int
    page: int
    page_size: int


class TutorQueryParams(BaseModel):
    page: int = 1
    page_size: int = 20
    search: Optional[str] = None
    role: str = "tutor"

    is_verified: Optional[bool] = None


class TutorDetailResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    avatar_url: Optional[str] = None

    role: Optional[RoleRead] = None
    tutor_profile: Optional[TutorProfileRead] = None

    model_config = {"from_attributes": True}


class TutorUserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None

class TutorProfileUpdate(BaseModel):
    headline: Optional[str] = None
    bio: Optional[str] = None

    experience_years: Optional[int] = None
    hourly_rate: Optional[float] = None

    is_verified: Optional[bool] = None


class TutorDeleteResponse(BaseModel):
    success: bool
    message: str
    deleted_user_id: UUID