from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.payment import Payment, PaymentStatus
from data_access.db.models.booking import Booking


async def seed_payments(db: AsyncSession):

    bookings = (await db.execute(select(Booking))).scalars().all()

    for booking in bookings:

        exists = await db.execute(
            select(Payment).where(Payment.booking_id == booking.id)
        )

        if exists.scalar_one_or_none():
            continue

        db.add(Payment(
            booking_id=booking.id,
            amount=50.00,
            currency="KZT",
            status=PaymentStatus.completed
        ))

    await db.commit()