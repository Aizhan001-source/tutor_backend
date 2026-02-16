from pydantic import BaseModel, EmailStr

# сериализация үшін
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re
from uuid import UUID


class UserCreate(BaseModel):
    first_name: str = Field(
        min_length=2,
        max_length=100,
        description="Имя пользователя"
    )

    last_name: str = Field(
        min_length=2,
        max_length=100,
        description="Фамилия пользователя"
    )

    email: EmailStr

    phone: Optional[str] = Field(
        default=None,
        pattern=r"^\+?[0-9]{10,15}$",
        description="Номер телефона в международном формате"
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="Пароль пользователя"
    )

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, value: str):
        if not value.isalpha():
            raise ValueError("Имя и фамилия должны содержать только буквы")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[a-z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r"[0-9]", value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return value


class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True
