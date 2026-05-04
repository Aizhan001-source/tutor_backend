# from fastapi import HTTPException
# from sqlalchemy import UUID
# from sqlalchemy.ext.asyncio import AsyncSession
# from api.tutors.tutor_schemas import EducationRead, TutorRead
# from api.users.user_schemas import UserRead
# from data_access.tutors.tutor_repository import TutorRepository


# class TutorService:
#     def __init__(self, db: AsyncSession):
#         self.repo = TutorRepository(db)

#     async def get_all_tutors(self):
#         tutors = await self.repo.get_all_tutors()

#         return [
#             TutorRead(
#                 id=tutor.id,
#                 bio=tutor.bio,
#                 experience_years=tutor.experience_years,
#                 education=EducationRead(
#                     id=tutor.education.id,
#                     name=tutor.education.name,
#                 ),
#                 user=UserRead(
#                     id=tutor.user.id,
#                     first_name=tutor.user.first_name,
#                     last_name=tutor.user.last_name,
#                     email=tutor.user.email,
#                 ),
#                 price_per_hour=tutor.price_per_hour,
#                 currency=tutor.currency,
#                 average_rating=tutor.average_rating,
#                 total_reviews=tutor.total_reviews,
#                 created_at=tutor.created_at,
#                 updated_at=tutor.updated_at,
#             ) for tutor in tutors
#         ]
    
#     async def get_tutor_by_id(self, tutor_id:UUID):
#         tutor = await self.repo.get_tutor_by_id(tutor_id)
        
#         if not tutor:
#             raise HTTPException(status_code=404, detail="tutor Not Found")
        
#         return TutorRead(
#             id=tutor.id,
#             bio=tutor.bio,
#             experience_years=tutor.experience_years,
#             education=EducationRead(
#                 id=tutor.education.id,
#                 name=tutor.education.name
#             ),
#             user=UserRead(
#                 id=tutor.user.id,
#                 first_name=tutor.user.first_name,
#                 last_name=tutor.user.last_name,
#                 email=tutor.user.email,
#             ),
#             price_per_hour=tutor.price_per_hour,
#             currency=tutor.currency,
#             average_rating=tutor.average_rating,
#             total_reviews=tutor.total_reviews,
#             created_at=tutor.created_at,
#             updated_at=tutor.updated_at,
#         )
    
#     async def get_tutors_count(self) -> int:
#         return await self.repo.get_tutors_count()

from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.tutors.tutor_schemas import EducationRead, TutorRead
from api.users.user_schemas import UserRead
from data_access.tutors.tutor_repository import TutorRepository
from data_access.db.models.tutor import Tutor


class TutorService:
    def __init__(self, db: AsyncSession):
        self.repo = TutorRepository(db)

    def _map_tutor(self, tutor: Tutor) -> TutorRead:
        return TutorRead(
            id=tutor.id,
            bio=tutor.bio,
            experience_years=tutor.experience_years,
            education=EducationRead(
                id=tutor.education.id,
                name=tutor.education.name,
            ),
            user=UserRead(
                id=tutor.user.id,
                first_name=tutor.user.first_name,
                last_name=tutor.user.last_name,
                email=tutor.user.email,
            ),
            price_per_hour=tutor.price_per_hour,
            currency=tutor.currency,
            average_rating=tutor.average_rating,
            total_reviews=tutor.total_reviews,
            created_at=tutor.created_at,
            updated_at=tutor.updated_at,
        )

    async def get_all_tutors(self) -> list[TutorRead]:
        tutors = await self.repo.get_all_tutors()
        return [self._map_tutor(t) for t in tutors]

    async def get_tutor_by_id(self, tutor_id: UUID) -> TutorRead:
        tutor = await self.repo.get_tutor_by_id(tutor_id)
        if not tutor:
            raise HTTPException(status_code=404, detail="Tutor Not Found")
        return self._map_tutor(tutor)

    async def get_by_user_id(self, user_id: UUID) -> TutorRead | None:
        tutor = await self.repo.get_by_user_id(user_id)
        if not tutor:
            return None
        return self._map_tutor(tutor)

    async def get_tutors_count(self) -> int:
        return await self.repo.get_tutors_count()