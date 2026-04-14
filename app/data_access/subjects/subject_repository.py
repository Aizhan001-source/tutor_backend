from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from data_access.db.models.subject import Subject


class SubjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all(self) -> list[Subject]:
        result = await self.db.execute(select(Subject))
        return result.scalars().all()
    
    async def get_by_id(self, subject_id: str) -> Subject | None:
        result =  await self.db.execute(select(Subject).where(Subject.id == subject_id))
        return result.scalar_one_or_none()
    
    async def search_by_name(self, name: str) -> list[Subject]:
        result = await self.db.execute(select(Subject).where(Subject.name.ilike(f"%{name}%")))
        return result.scalars().all()
    

    async def create(self, subject: Subject) -> Subject:
        self.db.add(subject)
        await self.db.commit()
        await self.db.refresh(subject)
        return subject