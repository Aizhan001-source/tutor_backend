from uuid import UUID
from fastapi import HTTPException

from data_access.favorites.favorite_repository import FavoriteRepository
from data_access.tutors.tutor_repository import TutorRepository


class FavoriteService:
    def __init__(self, fav_repo: FavoriteRepository, tutor_repo: TutorRepository):
        self.fav_repo = fav_repo
        self.tutor_repo = tutor_repo

    async def add(self, student_id: UUID, tutor_id: UUID):
        tutor = await self.tutor_repo.get_tutor_by_id(tutor_id)

        if not tutor:
            raise HTTPException(status_code=404, detail="Tutor not found")

        exists = await self.fav_repo.exists(student_id, tutor_id)
        if exists:
            raise HTTPException(status_code=400, detail="Already in favorites")

        return await self.fav_repo.add(student_id, tutor_id)

    async def remove(self, student_id: UUID, tutor_id: UUID):
        return await self.fav_repo.remove(student_id, tutor_id)

    async def get_my(self, student_id: UUID):
        return await self.fav_repo.get_by_student(student_id)