from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data_access.db.models.user import User
from data_access.db.models.student_profiles import StudentProfile
from data_access.db.models.role import Role


class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_students(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
    ) -> Tuple[List[User], int]:

        stmt = (
            select(User)
            .options(
                selectinload(User.role),
                selectinload(User.student_profile),
            )
            .join(Role, User.role_id == Role.id)
            .where(Role.name == "student")
        )

        if search:
            stmt = stmt.where(
                or_(
                    User.first_name.ilike(f"%{search}%"),
                    User.last_name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            )

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar()

        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(stmt)
        students = result.scalars().unique().all()

        return students, total

    async def get_student_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = (
            select(User)
            .options(
                selectinload(User.role),
                selectinload(User.student_profile),
            )
            .where(User.id == user_id)
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user(self, user_id: UUID, data: dict) -> Optional[User]:
        user = await self.get_student_by_id(user_id)
        if not user:
            return None

        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_profile(self, user_id: UUID, data: dict) -> Optional[StudentProfile]:
        stmt = select(StudentProfile).where(StudentProfile.user_id == user_id)
        result = await self.db.execute(stmt)
        profile = result.scalar_one_or_none()

        if not profile:
            return None

        for key, value in data.items():
            if value is not None:
                setattr(profile, key, value)

        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def delete_student(self, user_id: UUID) -> bool:
        user = await self.get_student_by_id(user_id)
        if not user:
            return False

        await self.db.delete(user)
        await self.db.commit()
        return True