from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from data_access.db.models.course import Course


class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_courses(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
    ) -> Tuple[List[Course], int]:

        stmt = select(Course)

        # search filter
        if search:
            stmt = stmt.where(
                or_(
                    Course.title.ilike(f"%{search}%"),
                    Course.description.ilike(f"%{search}%"),
                )
            )

        # count query
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar()

        # pagination
        stmt = stmt.order_by(Course.created_at.desc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(stmt)
        courses = result.scalars().all()

        return courses, total

    async def get_by_id(self, course_id: UUID) -> Optional[Course]:
        result = await self.db.execute(
            select(Course).where(Course.id == course_id)
        )
        return result.scalar_one_or_none()

    async def create(self, course: Course) -> Course:
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def update(self, course: Course) -> Course:
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def delete(self, course: Course) -> None:
        await self.db.delete(course)
        await self.db.commit()