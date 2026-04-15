from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.session import get_db
from data_access.application.application_repository import TutorApplicationRepository
from business_logic.application.application_service import TutorApplicationService

from api.application.application_schemas import (
    TutorApplicationListResponse,
    TutorApplicationRead,
    TutorApplicationQueryParams,
    TutorApplicationReviewRequest,
    TutorApplicationReviewResponse,
)

from utils.auth_middleware import get_current_user


router = APIRouter()


# =========================
# 🔧 DEPENDENCY INJECTION
# =========================
def get_application_service(
    db: AsyncSession = Depends(get_db),
) -> TutorApplicationService:
    return TutorApplicationService(db)


# =========================
# 📄 GET APPLICATIONS LIST
# =========================
@router.get("/", response_model=TutorApplicationListResponse)
async def get_applications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = Query("pending"),
    search: str | None = Query(None),
    service: TutorApplicationService = Depends(get_application_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    params = TutorApplicationQueryParams(
        page=page,
        page_size=page_size,
        status=status,
        search=search,
    )

    return await service.get_applications(params)


# =========================
# 🔎 GET APPLICATION BY ID
# =========================
@router.get("/{application_id}", response_model=TutorApplicationRead)
async def get_application(
    application_id: UUID = Path(...),
    service: TutorApplicationService = Depends(get_application_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.get_application(application_id)


# =========================
# ✅ REVIEW APPLICATION (APPROVE / REJECT)
# =========================
@router.patch(
    "/{application_id}/review",
    response_model=TutorApplicationReviewResponse,
)
async def review_application(
    application_id: UUID,
    data: TutorApplicationReviewRequest,
    service: TutorApplicationService = Depends(get_application_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.review_application(
        application_id=application_id,
        data=data,
        reviewer_id=user.id,
    )