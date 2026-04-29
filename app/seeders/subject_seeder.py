from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data_access.db.models.subject import Subject


async def seed_subjects(db: AsyncSession):
    subjects = ["Math", "Physics", "English"]

    for name in subjects:
        result = await db.execute(
            select(Subject).where(Subject.name == name)
        )

        if not result.scalar_one_or_none():
            db.add(Subject(name=name))

    await db.commit()   