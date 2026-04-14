from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.payments import Payment, PaymentStatus
from data_access.payments.payment_repository import PaymentRepository
from api.payments.payment_schemas import PaymentCreate


class PaymentService:
    def __init__(self, repo: PaymentRepository):
        self.repo = repo

    async def create_payment(
            self,
            student_id: UUID, 
            booking_id: UUID,
            amount,
            currency:str
            ):
        return await self.repo.create_payment(
            student_id=student_id,
            booking_id=booking_id,
            amount=amount,
            currency=currency,
            status=PaymentStatus.pending
        )
    
    async def get_by_id(self, payment_id: UUID):
        return await self.repo.get_by_id(payment_id)
    
    async def get_payments_by_student(self, student_id: UUID):
        return await self.repo.get_by_student(student_id)
        