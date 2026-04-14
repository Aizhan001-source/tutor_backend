from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.payments import Payment, PaymentStatus
from data_access.db.models.bookings import Booking

async def seed_payments(db: AsyncSession):
    bookings_result = await db.execute(select(Booking))
    bookings = bookings_result.scalars().all()

    for booking in bookings:
        # Проверка, есть ли уже платеж для бронирования
        result = await db.execute(select(Payment).where(Payment.booking_id == booking.id))
        if not result.scalar_one_or_none():
            payment = Payment(
                booking_id=booking.id,
                amount=50,  # пример фиксированной суммы
                status=PaymentStatus.PAID
            )
            db.add(payment)

    await db.commit()
    print("Payments seeded!")