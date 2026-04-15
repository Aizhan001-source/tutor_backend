from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from data_access.db.models.user import User
from data_access.db.models.role import Role
from data_access.db.models.sessions import Session
from data_access.db.models.payments import Payment


class AdminStatsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_students(self) -> int:
        result = await self.db.execute(
            select(func.count(User.id))
            .join(Role)
            .where(Role.name == "student")
        )
        return result.scalar()

    async def count_tutors(self) -> int:
        result = await self.db.execute(
            select(func.count(User.id))
            .join(Role)
            .where(Role.name == "tutor")
        )
        return result.scalar()

    async def count_active_sessions(self) -> int:
        result = await self.db.execute(
            select(func.count(Session.id))
            .where(Session.is_active == True)
        )
        return result.scalar()

    async def revenue_mtd(self) -> float:
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        result = await self.db.execute(
            select(func.coalesce(func.sum(Payment.amount), 0))
            .where(Payment.created_at >= start_of_month)
        )
        return result.scalar()