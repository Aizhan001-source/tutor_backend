from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.favorite import Favorite


class FavoriteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_to_favorite(self, student_id: UUID, tutor_id: UUID):
        favorite = Favorite(
            student_id=student_id,
            tutor_id=tutor_id
        )
        self.db.add(favorite)
        await self.db.commit()
        await self.db.refresh(favorite)
        return favorite

    async def get_favorite(self, student_id: UUID, tutor_id: UUID):
        stmt = select(Favorite).where(
            Favorite.student_id == student_id,
            Favorite.tutor_id == tutor_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_student(self, student_id: UUID):
        stmt = select(Favorite).where(Favorite.student_id == student_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def remove_from_favorite(self, student_id: UUID, tutor_id: UUID):
        stmt = delete(Favorite).where(
            Favorite.student_id == student_id,
            Favorite.tutor_id == tutor_id
        )
        await self.db.execute(stmt)
        await self.db.commit()