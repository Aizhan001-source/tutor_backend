from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data_access.db.models.tutor_applications import TutorApplication
from data_access.db.models.user import User


class TutorApplicationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_applications(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = "pending",
        search: Optional[str] = None,
    ) -> Tuple[List[TutorApplication], int]:

        stmt = (
            select(TutorApplication)
            .options(
                selectinload(TutorApplication.user),
                selectinload(TutorApplication.reviewer),
            )
        )

        # filter by status
        if status:
            stmt = stmt.where(TutorApplication.status == status)

        # search by user fields
        if search:
            stmt = stmt.join(User, TutorApplication.user_id == User.id).where(
                or_(
                    User.first_name.ilike(f"%{search}%"),
                    User.last_name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            )

        # count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar()

        # pagination
        stmt = stmt.order_by(TutorApplication.created_at.desc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(stmt)
        applications = result.scalars().unique().all()

        return applications, total

    async def get_by_id(self, application_id: UUID) -> Optional[TutorApplication]:

        stmt = (
            select(TutorApplication)
            .options(
                selectinload(TutorApplication.user),
                selectinload(TutorApplication.reviewer),
            )
            .where(TutorApplication.id == application_id)
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_status(
        self,
        application_id: UUID,
        status: str,
        reviewer_id: UUID,
    ) -> Optional[TutorApplication]:

        application = await self.get_by_id(application_id)

        if not application:
            return None

        application.status = status
        application.reviewed_by = reviewer_id
        application.reviewed_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(application)

        return application