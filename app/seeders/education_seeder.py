from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data_access.db.models.education import Education


async def seed_educations(db: AsyncSession):
    educations = ["bachelor", "master", "doctor"]

    for name in educations:
        exists = await db.execute(select(Education).where(Education.name == name))
        if not exists.scalar_one_or_none():
            db.add(Education(name=name))

    await db.commit()