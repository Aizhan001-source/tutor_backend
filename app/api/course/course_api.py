from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.session import get_db
from data_access.course.course_repository import CourseRepository
from business_logic.course.course_service import CourseService

from api.course.course_schemas import (
    CourseCreate,
    CourseRead,
    CourseUpdate,
)

from utils.auth_middleware import get_current_user


router = APIRouter()


# =========================
# 🔧 DEPENDENCY INJECTION
# =========================
def get_course_service(
    db: AsyncSession = Depends(get_db),
) -> CourseService:
    return CourseService(db)


# =========================
# 📄 GET ALL COURSES
# =========================
@router.get("/")
async def get_courses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    service: CourseService = Depends(get_course_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.get_courses(
        page=page,
        page_size=page_size,
        search=search,
    )


# =========================
# 🔎 GET COURSE BY ID
# =========================
@router.get("/{course_id}", response_model=CourseRead)
async def get_course_by_id(
    course_id: UUID = Path(...),
    service: CourseService = Depends(get_course_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.get_by_id(course_id)


# =========================
# ➕ CREATE COURSE
# =========================
@router.post("/", response_model=CourseRead)
async def create_course(
    data: CourseCreate,
    service: CourseService = Depends(get_course_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.create_course(data)


# =========================
# ✏️ UPDATE COURSE
# =========================
@router.patch("/{course_id}", response_model=CourseRead)
async def update_course(
    course_id: UUID,
    data: CourseUpdate,
    service: CourseService = Depends(get_course_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.update_course(course_id, data)


# =========================
# 🗑️ DELETE COURSE
# =========================
@router.delete("/{course_id}")
async def delete_course(
    course_id: UUID,
    service: CourseService = Depends(get_course_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.delete_course(course_id)