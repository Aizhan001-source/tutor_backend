from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy.orm import selectinload

from data_access.db.models.tutor import Tutor


class TutorRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(
            select(Tutor).options(selectinload(Tutor.user))
            )
        return result.scalars().all()

    async def get_by_id(self, tutor_id: UUID):
        result = await self.db.execute(
            select(Tutor).where(Tutor.id == tutor_id)
            .options(selectinload(Tutor.user))
        )
        return result.scalar_one_or_none()

    async def create(self, data):
        tutor = Tutor(
            user_id=data.user_id,
            bio=data.bio,
            experience_years=data.experience_years,
            education=data.education,
            price_per_hour=data.price_per_hour,
            currency=data.currency,
            format=data.format,
            city=data.city,
        )
        self.db.add(tutor)
        await self.db.commit()
        await self.db.refresh(tutor)
        return tutor

    async def update(self, tutor: Tutor):
        await self.db.commit()
        await self.db.refresh(tutor)
        return tutor

    async def delete(self, tutor: Tutor):
        await self.db.delete(tutor)
        await self.db.commit()
        return True