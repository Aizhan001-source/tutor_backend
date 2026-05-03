from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.booking import Booking
from data_access.db.models.student import Student
from data_access.db.models.schedule import Schedule


async def seed_bookings(db: AsyncSession):
    students = (await db.execute(select(Student))).scalars().all()
    schedules = (await db.execute(select(Schedule))).scalars().all()

    for student in students:
        for schedule in schedules[:1]: 
            exists = await db.execute(
                select(Booking).where(
                    Booking.student_id == student.id,
                    Booking.schedule_id == schedule.id
                )
            )

            if exists.scalar_one_or_none():
                continue

            db.add(Booking(
                student_id=student.id,
                schedule_id=schedule.id,
                status="confirmed"
            ))

    await db.commit()