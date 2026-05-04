from uuid import UUID
from fastapi import HTTPException

from data_access.favorites.favorite_repository import FavoriteRepository
from data_access.tutors.tutor_repository import TutorRepository


class FavoriteService:
    def __init__(self, fav_repo: FavoriteRepository, tutor_repo: TutorRepository):
        self.fav_repo = fav_repo
        self.tutor_repo = tutor_repo

    async def add(self, student_id: UUID, tutor_id: UUID):
        print("ADD FAVORITE:", student_id, tutor_id)

        tutor = await self.tutor_repo.get_tutor_by_id(tutor_id)

        if not tutor:
            print("NO TUTOR")
            raise HTTPException(404)

        exists = await self.fav_repo.exists(student_id, tutor_id)
        print("EXISTS:", exists)

        return await self.fav_repo.add(student_id, tutor_id)
    
    async def remove(self, student_id: UUID, tutor_id: UUID):
        return await self.fav_repo.remove(student_id, tutor_id)

    async def get_my(self, student_id: UUID):
        return await self.fav_repo.get_by_student(student_id)