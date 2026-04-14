from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from api.tutors.tutor_schemas import TutorCreate, TutorRead, TutorUpdate
from data_access.db.session import get_db
from data_access.tutors.tutor_repository import TutorRepository
from business_logic.tutors.tutor_service import TutorService
from utils.auth_middleware import get_current_user
from api.users.user_schemas import CurrentUser

router = APIRouter()


def get_tutor_service(db: AsyncSession = Depends(get_db)):
    return TutorService(TutorRepository(db))


# -----------------------
# GET ALL
# -----------------------
@router.get("/", response_model=list[TutorRead])
async def get_all_tutors(
    service: TutorService = Depends(get_tutor_service)
):
    return await service.get_all()


# -----------------------
# GET BY ID
# -----------------------
@router.get("/{tutor_id}", response_model=TutorRead)
async def get_tutor(
    tutor_id: UUID,
    service: TutorService = Depends(get_tutor_service),
):
    tutor = await service.get_by_id(tutor_id)

    if not tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tutor not found"
        )

    return tutor


# -----------------------
# CREATE (ONLY ADMIN)
# -----------------------
@router.post("/", response_model=TutorRead, status_code=201)
async def create_tutor(
    tutor: TutorCreate,
    current_user: CurrentUser = Depends(get_current_user),
    service: TutorService = Depends(get_tutor_service),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can create tutors"
        )

    return await service.create(tutor)


# -----------------------
# UPDATE
# -----------------------
@router.patch("/{tutor_id}", response_model=TutorRead)
async def update_tutor(
    tutor_id: UUID,
    data: TutorUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    service: TutorService = Depends(get_tutor_service),
):
    tutor = await service.get_by_id(tutor_id)

    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")

    if current_user.role != "admin" and current_user.id != tutor.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return await service.update(tutor_id, data)


# -----------------------
# DELETE
# -----------------------
@router.delete("/{tutor_id}")
async def delete_tutor(
    tutor_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: TutorService = Depends(get_tutor_service),
):
    tutor = await service.get_by_id(tutor_id)

    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete tutors")

    await service.delete(tutor_id)
    return {"message": "Tutor deleted"}