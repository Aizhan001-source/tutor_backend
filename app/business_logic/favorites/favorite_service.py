from uuid import UUID
from fastapi import HTTPException

from data_access.favorites.favorite_repository import FavoriteRepository


class FavoriteService:
    def __init__(self, repo: FavoriteRepository):
        self.repo = repo

    async def add_to_favorite(self, student_id: UUID, tutor_id: UUID):
        existing = await self.repo.get_favorite(student_id, tutor_id)

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Tutor already in favorites"
            )

        return await self.repo.add_to_favorite(student_id, tutor_id)

    async def remove_from_favorite(self, student_id: UUID, tutor_id: UUID):
        existing = await self.repo.get_favorite(student_id, tutor_id)

        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Favorite not found"
            )

        await self.repo.remove_from_favorite(student_id, tutor_id)

    async def get_my_favorites(self, student_id: UUID):
        return await self.repo.get_by_student(student_id)