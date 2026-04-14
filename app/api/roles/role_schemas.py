from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    tutor = "tutor"
    student = "student"
    
class RoleRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None  # поле description тоже добавим

    model_config = {"from_attributes": True}  # чтобы создавать из ORM объектов


