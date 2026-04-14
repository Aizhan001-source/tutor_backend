from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class RoleRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None  # поле description тоже добавим

    model_config = {"from_attributes": True}  # чтобы создавать из ORM объектов