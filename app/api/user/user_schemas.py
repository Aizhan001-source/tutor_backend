from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    avatar_url: Optional[str] = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserProfileRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    avatar_url: Optional[str] = None
    status: str

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    avatar_url: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    status: Optional[str] = None

    old_password: Optional[str] = None
    new_password: Optional[str] = None