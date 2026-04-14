from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.tutor import Tutor
from data_access.db.models.user import User


async def seed_tutors(db: AsyncSession):
    tutors_data = [
        {"user_email": "alice@example.com", "bio": "Math tutor", "hourly_rate": 30},
        {"user_email": "bob@example.com", "bio": "Physics tutor", "hourly_rate": 35},
    ]


    for t in tutors_data:
        result = await db.execute(select(User).where(User.email == t["user_email"]))
        user = result.scalar_one_or_none()
        if user:
            exists = await db.execute(select(Tutor).where(Tutor.user_id == user.id))
            if not exists.scalar_one_or_none():
                tutor = Tutor(
                    user_id=user.id,
                    bio=t["bio"],
                    hourly_rate=t["hourly_rate"]
                )
                db.add(tutor)


    await db.commit()
    print("Tutors seeded!")