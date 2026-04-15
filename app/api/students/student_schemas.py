from typing import Optional, List
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class RoleRead(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}



class StudentProfileRead(BaseModel):
    id: UUID
    user_id: UUID

    level: str
    learning_goals: Optional[list] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None
    preferred_language: Optional[str] = None

    total_sessions: int
    completed_sessions: int
    total_spent_hours: int
    last_session_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class StudentUserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    avatar_url: Optional[str] = None

    role: Optional[RoleRead] = None
    student_profile: Optional[StudentProfileRead] = None

    model_config = {"from_attributes": True}

class StudentListResponse(BaseModel):
    items: List[StudentUserRead]

    total: int
    page: int
    page_size: int


class StudentQueryParams(BaseModel):
    page: int = 1
    page_size: int = 20
    search: Optional[str] = None
    role: str = "student"

class StudentDetailResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    avatar_url: Optional[str] = None

    role: Optional[RoleRead] = None
    student_profile: Optional[StudentProfileRead] = None

    model_config = {"from_attributes": True}


class StudentUserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None


class StudentProfileUpdate(BaseModel):
    level: Optional[str] = None
    learning_goals: Optional[list] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None
    preferred_language: Optional[str] = None


class StudentDeleteResponse(BaseModel):
    success: bool
    message: str
    deleted_user_id: UUID