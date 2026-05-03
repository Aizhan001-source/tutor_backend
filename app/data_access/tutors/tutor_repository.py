from typing import List
from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data_access.db.models.tutor import Tutor


class TutorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_tutors(self) -> List [Tutor]:
        result = await self.db.execute(
            select(Tutor).options(
                selectinload(Tutor.education),
                selectinload(Tutor.user),
            )
        )
        return result.scalars().all()
    
    
    async def get_tutor_by_id(self, tutor_id:UUID):
        result = await self.db.execute(
            select(Tutor).where(Tutor.id == tutor_id)
            .options(selectinload(Tutor.user))
            .options(selectinload(Tutor.education))
        )
        return result.scalar_one_or_none()