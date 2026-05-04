# from fastapi import APIRouter, Depends, HTTPException
# from uuid import UUID
# from sqlalchemy.ext.asyncio import AsyncSession
# from business_logic.tutors.tutor_service import TutorService
# from api.tutors.tutor_schemas import TutorRead
# from data_access.db.session import get_db

# router = APIRouter()

# def get_tutor_service(db: AsyncSession = Depends(get_db)) -> TutorService:
#     return TutorService(db)

# @router.get("/all", response_model=list[TutorRead])
# async def get_all_tutors(
#     service: TutorService = Depends(get_tutor_service),
# ):
#     return await service.get_all_tutors()
    
# @router.get("/count")
# async def get_tutors_count(
#     service: TutorService = Depends(get_tutor_service),
# ):
#     return await service.get_tutors_count()

# @router.get("/by_id/{tutor_id}", response_model=TutorRead)
# async def get_tutor_by_id(
#     tutor_id: UUID,
#     service: TutorService = Depends(get_tutor_service),
# ):
#     tutor = await service.get_tutor_by_id(tutor_id)

#     if not tutor:
#         raise HTTPException (
#             status_code=404,detail="Tutor Not Found"
#             )

#     return tutor
    
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from business_logic.tutors.tutor_service import TutorService
from api.tutors.tutor_schemas import TutorRead
from data_access.db.session import get_db
from utils.auth_middleware import get_current_user

router = APIRouter()

def get_tutor_service(db: AsyncSession = Depends(get_db)) -> TutorService:
    return TutorService(db)

@router.get("/all", response_model=list[TutorRead])
async def get_all_tutors(
    service: TutorService = Depends(get_tutor_service),
):
    return await service.get_all_tutors()

@router.get("/count")
async def get_tutors_count(
    service: TutorService = Depends(get_tutor_service),
):
    return await service.get_tutors_count()

@router.get("/me", response_model=TutorRead)
async def get_my_tutor_profile(
    current_user=Depends(get_current_user()),  # ← скобки!
    service: TutorService = Depends(get_tutor_service),
):
    tutor = await service.get_by_user_id(current_user["user_id"])
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor profile not found")
    return tutor

@router.get("/by-user/{user_id}", response_model=TutorRead)
async def get_tutor_by_user(
    user_id: UUID,
    service: TutorService = Depends(get_tutor_service),
):
    tutor = await service.get_by_user_id(user_id)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")
    return tutor

@router.get("/by_id/{tutor_id}", response_model=TutorRead)
async def get_tutor_by_id(
    tutor_id: UUID,
    service: TutorService = Depends(get_tutor_service),
):
    tutor = await service.get_tutor_by_id(tutor_id)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor Not Found")
    return tutor