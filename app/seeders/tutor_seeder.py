from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.tutor import Tutor
from data_access.db.models.user import User
from data_access.db.models.subject import Subject


async def seed_tutors(db: AsyncSession):

    tutors_data = [
        {
            "user_email": "alice@example.com",
            "subject": "Math",
            "bio": "Math tutor",
            "price": 30,
        },
        {
            "user_email": "bob@example.com",
            "subject": "Physics",
            "bio": "Physics tutor",
            "price": 35,
        }
    ]

    for t in tutors_data:

        subject = await db.execute(
            select(Subject).where(Subject.name == t["subject"])
        )
        subject = subject.scalar_one_or_none()

        if not subject:
            raise Exception(f"Subject {t['subject']} not found")

        user = await db.execute(
            select(User).where(User.email == t["user_email"])
        )
        user = user.scalar_one_or_none()

        if not user:
            continue

        exists = await db.execute(
            select(Tutor).where(Tutor.user_id == user.id)
        )

        if exists.scalar_one_or_none():
            continue

        db.add(Tutor(
            user_id=user.id,
            subject_id=subject.id,
            bio=t["bio"],
            price_per_hour=t["price"],
            currency="KZT",
            format="online",   # 🔥 ОБЯЗАТЕЛЬНО
            experience_years=2,
            education="Bachelor",
            city="Karaganda",
        ))

    await db.commit()