from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data_access.db.models.favorite import Favorite
from data_access.db.models.tutor import Tutor


class FavoriteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, student_id: UUID, tutor_id: UUID):
        favorite = Favorite(student_id=student_id, tutor_id=tutor_id)

        self.db.add(favorite)
        await self.db.commit()
        await self.db.refresh(favorite)

        return favorite

    async def remove(self, student_id: UUID, tutor_id: UUID):
        await self.db.execute(
            delete(Favorite).where(
                Favorite.student_id == student_id,
                Favorite.tutor_id == tutor_id
            )
        )
        await self.db.commit()

    async def get_by_student(self, student_id: UUID):
        query = (
            select(Favorite)
            .where(Favorite.student_id == student_id)
            .options(
                selectinload(Favorite.tutor).selectinload(Tutor.user),
                selectinload(Favorite.tutor).selectinload(Tutor.education),
            )
        )

        result = await self.db.execute(query)
        return result.scalars().unique().all()

    async def exists(self, student_id: UUID, tutor_id: UUID) -> bool:
        result = await self.db.execute(
            select(Favorite).where(
                Favorite.student_id == student_id,
                Favorite.tutor_id == tutor_id
            )
        )
        return result.scalar_one_or_none() is not None