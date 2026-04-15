from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class TutorApplicationStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class TutorApplicationUserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str

    model_config = {"from_attributes": True}

class TutorApplicationRead(BaseModel):
    id: UUID

    user_id: UUID
    status: str

    created_at: datetime

    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None

    user: Optional[TutorApplicationUserRead] = None

    model_config = {"from_attributes": True}

class TutorApplicationListResponse(BaseModel):
    items: List[TutorApplicationRead]

    total: int
    page: int
    page_size: int


class TutorApplicationQueryParams(BaseModel):
    page: int = 1
    page_size: int = 20

    status: Optional[str] = "pending"
    search: Optional[str] = None


class TutorApplicationReviewRequest(BaseModel):
    status: str  # "approved" | "rejected"


class TutorApplicationReviewResponse(BaseModel):
    id: UUID
    status: str

    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None

    message: str