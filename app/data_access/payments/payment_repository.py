from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.payment import Payment
from data_access.db.models.booking import Booking


class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payment: Payment):
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_by_id(self, payment_id: UUID):
        result = await self.db.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: UUID):
        result = await self.db.execute(
            select(Payment)
            .join(Payment.booking)
            .where(Booking.student_id == user_id)
        )
        return result.scalars().all()