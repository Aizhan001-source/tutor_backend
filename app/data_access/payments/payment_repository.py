from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.payments import Payment


class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(
            self, 
            student_id: UUID, 
            booking_id: UUID, 
            amount, 
            currency, 
            status
        ):
        payment = Payment(
            student_id=student_id,
            booking_id=booking_id,
            amount=amount,
            currency=currency,
            status=status
        )

        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)

    async def get_by_id(self, payment_id: UUID):
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        return result.scalar_one_or_none()
    

    async def get_by_student(self, student_id: UUID):
        result = await self.db.execute(select(Payment).join(Payment.booking).where(Payment.booking.student_id == student_id))

        return result.scalars().all()