from uuid import UUID
from fastapi import HTTPException

from data_access.subjects.subject_repository import SubjectRepository
from data_access.db.models.subject import Subject


class SubjectService:
    def __init__(self, repo: SubjectRepository):
        self.repo = repo


    async def create(self, name: str):
        name = name.strip().lower()

        existing = await self.repo.get_by_name(name)
        if existing:
            raise HTTPException(status_code=400, detail="Subject already exists")

        subject = Subject(name=name)
        return await self.repo.create(subject)

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, subject_id: UUID):
        subject = await self.repo.get_by_id(subject_id)

        if not subject:
            raise HTTPException(
                status_code=404,
                detail="Subject not found"
            )

        return subject

    async def delete(self, subject_id: UUID):
        subject = await self.repo.get_by_id(subject_id)

        if not subject:
            raise HTTPException(
                status_code=404,
                detail="Subject not found"
            )

        await self.repo.delete(subject)

    async def update(self, subject_id: UUID, name: str):
        subject = await self.repo.get_by_id(subject_id)

        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        subject.name = name.strip().lower()

        return await self.repo.update(subject)