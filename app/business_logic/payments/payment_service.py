from uuid import UUID
from fastapi import HTTPException

from data_access.payments.payment_repository import PaymentRepository
from data_access.db.models.payment import PaymentStatus


class PaymentService:
    def __init__(self, repo: PaymentRepository):
        self.repo = repo

    async def create_payment(
        self,
        student_id: UUID,
        booking_id: UUID,
        amount,
        currency: str
    ):
        return await self.repo.create_payment(
            student_id=student_id,
            booking_id=booking_id,
            amount=amount,
            currency=currency,
            status=PaymentStatus.pending
        )

    async def complete_payment(self, payment_id: UUID):
        payment = await self.repo.get_by_id(payment_id)

        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        payment.status = PaymentStatus.completed

        # бизнес-логика
        if payment.booking:
            payment.booking.status = "confirmed"

        return await self.repo.update(payment)

    async def get_by_id(self, payment_id: UUID):
        payment = await self.repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment

    async def get_payments_by_student(self, student_id: UUID):
        return await self.repo.get_by_student(student_id)