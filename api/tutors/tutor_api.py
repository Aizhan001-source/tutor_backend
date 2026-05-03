from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from business_logic.tutors.tutor_service import TutorService
from api.tutors.tutor_schemas import TutorRead
from data_access.db.session import get_db

router = APIRouter()

def get_tutor_service(db: AsyncSession = Depends(get_db)) -> TutorService:
    return TutorService(db)

@router.get("/all", response_model=list[TutorRead])
async def get_all_tutors(
    service: TutorService = Depends(get_tutor_service),
):
    return await service.get_all_tutors()

@router.get("/by_id/{tutor_id}", response_model=TutorRead)
async def get_tutor_by_id(
    tutor_id: UUID,
    service: TutorService = Depends(get_tutor_service),
):
    tutor = await service.get_tutor_by_id(tutor_id)

    if not tutor:
        raise HTTPException (
            status_code=404,detail="Tutor Not Found"
            )

    return tutor
    