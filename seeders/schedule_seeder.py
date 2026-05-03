from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from data_access.db.models.schedule import Schedule
from data_access.db.models.course import Course


async def seed_schedules(db: AsyncSession):
    courses = (await db.execute(select(Course))).scalars().all()

    for course in courses:
        exists = await db.execute(
            select(Schedule).where(Schedule.course_id == course.id)
        )

        if exists.scalar_one_or_none():
            continue

        db.add_all([
            Schedule(
                course_id=course.id,
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow() + timedelta(hours=1),
                is_available=True
            ),
            Schedule(
                course_id=course.id,
                start_time=datetime.utcnow() + timedelta(days=1),
                end_time=datetime.utcnow() + timedelta(days=1, hours=1),
                is_available=True
            )
        ])

    await db.commit()