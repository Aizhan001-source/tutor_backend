from datetime import datetime, timedelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.booking import Booking, BookingStatus
from data_access.db.models.user import User
from data_access.db.models.tutor import Tutor


async def seed_bookings(db: AsyncSession):

    students = (await db.execute(
        select(User).where(User.role.has(name="student"))
    )).scalars().all()

    tutors = (await db.execute(select(Tutor))).scalars().all()

    if not students or not tutors:
        return

    for i, student in enumerate(students):
        tutor = tutors[i % len(tutors)]

        start = datetime.utcnow() + timedelta(days=i + 1)
        end = start + timedelta(hours=1)

        exists = await db.execute(
            select(Booking).where(
                and_(
                    Booking.student_id == student.id,
                    Booking.tutor_id == tutor.user_id,
                    Booking.start_time == start
                )
            )
        )

        if exists.scalar_one_or_none():
            continue

        db.add(Booking(
            student_id=student.id,
            tutor_id=tutor.user_id,
            start_time=start,
            end_time=end,
            status=BookingStatus.pending
        ))

    await db.commit()