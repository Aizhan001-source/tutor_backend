from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.models.course import Course
from data_access.course.course_repository import CourseRepository

from api.course.course_schemas import (
    CourseCreate,
    CourseRead,
    CourseUpdate,
)


class CourseService:
    def __init__(self, db: AsyncSession):
        self.repo = CourseRepository(db)

    async def get_courses(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
    ):
        courses, total = await self.repo.get_courses(
            page=page,
            page_size=page_size,
            search=search,
        )

        return {
            "items": [
                CourseRead.model_validate(course)
                for course in courses
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def get_by_id(self, course_id: UUID):
        course = await self.repo.get_by_id(course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        return CourseRead.model_validate(course)

    async def create_course(self, data: CourseCreate):
        course = Course(
            title=data.title,
            description=data.description,
            price=data.price,
        )

        created_course = await self.repo.create(course)

        return CourseRead.model_validate(created_course)

    async def update_course(self, course_id: UUID, data: CourseUpdate):
        course = await self.repo.get_by_id(course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        if data.title is not None:
            course.title = data.title

        if data.description is not None:
            course.description = data.description

        if data.price is not None:
            course.price = data.price

        updated_course = await self.repo.update(course)

        return CourseRead.model_validate(updated_course)

    async def delete_course(self, course_id: UUID):
        course = await self.repo.get_by_id(course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        await self.repo.delete(course)

        return {"message": "Course deleted successfully"}