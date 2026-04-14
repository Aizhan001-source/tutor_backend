from uuid import UUID
from data_access.tutors.tutor_repository import TutorRepository


class TutorService:

    def __init__(self, repo: TutorRepository):
        self.repo = repo

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, tutor_id: UUID):
        return await self.repo.get_by_id(tutor_id)

    async def create(self, data):
        return await self.repo.create(data)

    async def update(self, tutor_id: UUID, data):
        tutor = await self.repo.get_by_id(tutor_id)
        if not tutor:
            raise ValueError("Tutor not found")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(tutor, field, value)

        return await self.repo.update(tutor)

    async def delete(self, tutor_id: UUID):
        tutor = await self.repo.get_by_id(tutor_id)
        if not tutor:
            raise ValueError("Tutor not found")

        await self.repo.delete(tutor)