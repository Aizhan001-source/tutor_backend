from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.students.student_repository import StudentRepository


class StudentService:
    def __init__(self, db: AsyncSession):
        self.repo = StudentRepository(db)

    async def create_student(self, user_id):
        existing = await self.repo.get_by_user_id(user_id)
        if existing:
            raise HTTPException(400, "Student already exists")

        return await self.repo.create(user_id)

    async def get_student(self, student_id):
        student = await self.repo.get_by_id(student_id)
        if not student:
            raise HTTPException(404, "Student not found")
        return student

    async def get_all_students(self):
        return await self.repo.get_all()

    async def get_students_with_count(self):
        students = await self.repo.get_all()
        count = await self.repo.get_students_count()

        return {
            "students": students,
            "count": count
        }

async def get_by_user_id(self, user_id):
    from uuid import UUID
    return await self.repo.get_by_user_id(UUID(str(user_id)))
    

    async def delete(self, student):
        await self.repo.delete(student)

    
    async def get_students_count(self) -> int:
        return await self.repo.get_students_count()