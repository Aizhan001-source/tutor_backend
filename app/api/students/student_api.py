from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.session import get_db
from data_access.students.student_repository import StudentRepository
from business_logic.student.student_service import StudentService

from api.students.student_schemas import (
    StudentListResponse,
    StudentDetailResponse,
    StudentUserUpdate,
    StudentProfileUpdate,
    StudentDeleteResponse,
    StudentQueryParams,
)

from utils.auth_middleware import get_current_user


router = APIRouter()


# =========================
# 🔧 DEPENDENCY INJECTION
# =========================
def get_student_service(
    db: AsyncSession = Depends(get_db),
) -> StudentService:
    return StudentService(db)


# =========================
# 📄 GET ALL STUDENTS
# =========================
@router.get("/", response_model=StudentListResponse)
async def get_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    service: StudentService = Depends(get_student_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    params = StudentQueryParams(
        page=page,
        page_size=page_size,
        search=search,
    )

    return await service.get_students(params)


# =========================
# 🔎 GET STUDENT BY ID
# =========================
@router.get("/{user_id}", response_model=StudentDetailResponse)
async def get_student_detail(
    user_id: UUID = Path(...),
    service: StudentService = Depends(get_student_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.get_student_detail(user_id)


# =========================
# ✏️ UPDATE STUDENT USER
# =========================
@router.patch("/{user_id}/user")
async def update_student_user(
    user_id: UUID,
    data: StudentUserUpdate,
    service: StudentService = Depends(get_student_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.update_student_user(user_id, data)


# =========================
# ✏️ UPDATE STUDENT PROFILE
# =========================
@router.patch("/{user_id}/profile")
async def update_student_profile(
    user_id: UUID,
    data: StudentProfileUpdate,
    service: StudentService = Depends(get_student_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.update_student_profile(user_id, data)


# =========================
# 🗑️ DELETE STUDENT
# =========================
@router.delete("/{user_id}", response_model=StudentDeleteResponse)
async def delete_student(
    user_id: UUID,
    service: StudentService = Depends(get_student_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.delete_student(user_id)