from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.bookings import Booking, BookingStatus
from data_access.db.models.user import User
from data_access.db.models.tutor import Tutor

async def seed_bookings(db: AsyncSession):
    # Берем студентов и репетиторов
    students_result = await db.execute(select(User).where(User.role_id == 2))  # reader/student
    students = students_result.scalars().all()

    tutors_result = await db.execute(select(Tutor))
    tutors = tutors_result.scalars().all()

    for i, student in enumerate(students):
        tutor = tutors[i % len(tutors)]
        start_time = datetime.utcnow() + timedelta(days=i+1)
        end_time = start_time + timedelta(hours=1)

        # Проверка, есть ли уже такое бронирование
        result = await db.execute(
            select(Booking).where(Booking.student_id == student.id, Booking.tutor_id == tutor.id, Booking.start_time == start_time)
        )
        if not result.scalar_one_or_none():
            booking = Booking(
                student_id=student.id,
                tutor_id=tutor.user_id,
                start_time=start_time,
                end_time=end_time,
                status=BookingStatus.PENDING
            )
            db.add(booking)

    await db.commit()
    print("Bookings seeded!")