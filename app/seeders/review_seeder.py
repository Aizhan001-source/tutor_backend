import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.review import Review
from data_access.db.models.booking import Booking, BookingStatus


async def seed_reviews(db: AsyncSession):

    bookings = (await db.execute(
        select(Booking).where(Booking.status == BookingStatus.completed)
    )).scalars().all()

    comments = [
        "Great tutor",
        "Very helpful",
        "Excellent explanation",
        "Highly recommended"
    ]

    for booking in bookings:

        exists = await db.execute(
            select(Review).where(Review.booking_id == booking.id)
        )

        if exists.scalar_one_or_none():
            continue

        db.add(Review(
            student_id=booking.student_id,
            tutor_id=booking.tutor_id,
            booking_id=booking.id,
            rating=random.randint(4, 5),
            comment=random.choice(comments)
        ))

    await db.commit()