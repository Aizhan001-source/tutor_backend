from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.session import get_db
from data_access.tutor.tutor_repository import AdminTutorRepository
from business_logic.tutor.tutor_service import AdminTutorService

from api.tutor.tutor_schemas import (
    TutorListResponse,
    TutorDetailResponse,
    TutorUserUpdate,
    TutorProfileUpdate,
    TutorDeleteResponse,
)

from utils.auth_middleware import get_current_user


router = APIRouter()


# =========================
# 🔧 DEPENDENCY INJECTION
# =========================
def get_admin_tutor_service(
    db: AsyncSession = Depends(get_db),
) -> AdminTutorService:
    repo = AdminTutorRepository(db)
    return AdminTutorService(repo)


# =========================
# 📄 GET ALL TUTORS
# =========================
@router.get("/", response_model=TutorListResponse)
async def get_tutors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    is_verified: bool | None = Query(None),
    service: AdminTutorService = Depends(get_admin_tutor_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.get_tutors(
        page=page,
        page_size=page_size,
        search=search,
        is_verified=is_verified,
    )


# =========================
# 🔎 GET TUTOR BY ID
# =========================
@router.get("/{user_id}", response_model=TutorDetailResponse)
async def get_tutor_by_id(
    user_id: UUID = Path(...),
    service: AdminTutorService = Depends(get_admin_tutor_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    tutor = await service.get_tutor_by_id(user_id)

    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")

    return tutor


# =========================
# ✏️ UPDATE USER (BASIC INFO)
# =========================
@router.patch("/{user_id}/user")
async def update_tutor_user(
    user_id: UUID,
    data: TutorUserUpdate,
    service: AdminTutorService = Depends(get_admin_tutor_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    tutor = await service.get_tutor_by_id(user_id)

    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")

    updated = await service.update_user(tutor, data)
    return updated


# =========================
# ✏️ UPDATE PROFILE
# =========================
@router.patch("/{user_id}/profile")
async def update_tutor_profile(
    user_id: UUID,
    data: TutorProfileUpdate,
    service: AdminTutorService = Depends(get_admin_tutor_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    tutor = await service.get_tutor_by_id(user_id)

    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")

    if not tutor.tutor_profile:
        raise HTTPException(status_code=400, detail="Tutor profile not found")

    updated = await service.update_profile(tutor.tutor_profile, data)
    return updated


# =========================
# 🗑️ DELETE TUTOR
# =========================
@router.delete("/{user_id}", response_model=TutorDeleteResponse)
async def delete_tutor(
    user_id: UUID,
    service: AdminTutorService = Depends(get_admin_tutor_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    tutor = await service.get_tutor_by_id(user_id)

    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")

    return await service.delete_tutor(tutor)