from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    
    model_config = {"from_attributes": True}

class UserProfileRead(BaseModel):
    first_name: str
    last_name: str
    email: str

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str


class RoleRead(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}


class UserAllRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    avatar_url: Optional[str] = None
    role: Optional[RoleRead] = None  # связь с ролью

    model_config = {"from_attributes": True}


class UserAdminCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    avatar_url: Optional[str]
    role: str

class CurrentUser(BaseModel):
    id: UUID
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None