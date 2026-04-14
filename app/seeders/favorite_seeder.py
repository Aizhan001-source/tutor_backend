from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.favorite import Favorite
from data_access.db.models.user import User


async def seed_favorites(db: AsyncSession):

    students = (await db.execute(
        select(User).where(User.role.has(name="student"))
    )).scalars().all()

    tutors = (await db.execute(
        select(User).where(User.role.has(name="tutor"))
    )).scalars().all()

    if not students or not tutors:
        return

    for i, student in enumerate(students):
        tutor = tutors[i % len(tutors)]

        exists = await db.execute(
            select(Favorite).where(
                Favorite.user_id == student.id,
                Favorite.tutor_id == tutor.id
            )
        )

        if exists.scalar_one_or_none():
            continue

        db.add(Favorite(
            user_id=student.id,
            tutor_id=tutor.id
        ))

    await db.commit()