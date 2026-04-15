from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from data_access.db.models.user import User
from data_access.db.models.role import Role
from data_access.db.models.tutor_profiles import TutorProfile


class AdminTutorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # =========================
    # 📄 LIST TUTORS
    # =========================
    async def get_tutors(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        is_verified: bool | None = None,
    ):
        query = (
            select(User)
            .join(Role)
            .options(
                selectinload(User.role),
                selectinload(User.tutor_profile),
            )
            .where(Role.name == "tutor")
        )

        # 🔎 SEARCH
        if search:
            query = query.where(
                (User.first_name.ilike(f"%{search}%")) |
                (User.last_name.ilike(f"%{search}%")) |
                (User.email.ilike(f"%{search}%")) |
                (TutorProfile.headline.ilike(f"%{search}%"))
            )

        # 🎯 FILTER VERIFIED
        if is_verified is not None:
            query = query.join(TutorProfile).where(
                TutorProfile.is_verified == is_verified
            )

        # 📊 COUNT QUERY
        count_query = (
            select(func.count(User.id))
            .join(Role)
            .where(Role.name == "tutor")
        )

        if search:
            count_query = count_query.where(
                (User.first_name.ilike(f"%{search}%")) |
                (User.last_name.ilike(f"%{search}%")) |
                (User.email.ilike(f"%{search}%"))
            )

        if is_verified is not None:
            count_query = count_query.join(TutorProfile).where(
                TutorProfile.is_verified == is_verified
            )

        total = (await self.db.execute(count_query)).scalar()

        # 📄 PAGINATION
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await self.db.execute(query)
        tutors = result.scalars().unique().all()

        return tutors, total

    # =========================
    # 🔎 GET BY ID
    # =========================
    async def get_tutor_by_id(self, user_id):
        result = await self.db.execute(
            select(User)
            .join(Role)
            .options(
                selectinload(User.role),
                selectinload(User.tutor_profile),
            )
            .where(User.id == user_id)
            .where(Role.name == "tutor")
        )

        return result.scalar_one_or_none()

    # =========================
    # ✏️ UPDATE USER
    # =========================
    async def update_user(self, user: User):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # =========================
    # ✏️ UPDATE PROFILE
    # =========================
    async def update_profile(self, profile: TutorProfile):
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    # =========================
    # 🗑️ DELETE USER
    # =========================
    async def delete_user(self, user: User):
        await self.db.delete(user)
        await self.db.commit()
        return True