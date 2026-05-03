from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.education import Education
from data_access.db.models.tutor import Tutor
from data_access.db.models.user import User
from data_access.db.models.subject import Subject


async def seed_tutors(db: AsyncSession):

    tutors_data = [
        {
            "user_email": "alice@example.com",
            "subject": "Math",
            "education": "bachelor",
            "bio": "Math tutor",
            "price": 30,
            "price_per_hour": 5000,
            "currency": "kzt",
            "average_rating": 4,
            "total_reviews": 5,
        },
        {
            "user_email": "bob@example.com",
            "subject": "Physics",
            "education": "master",
            "bio": "Physics tutor",
            "price": 35,
            "price_per_hour": 7000,
            "currency": "kzt",
            "average_rating": 4,
            "total_reviews": 5,
        }
    ]

    for t in tutors_data:
        user = await db.execute(
            select(User).where(User.email == t["user_email"])
        )
        user = user.scalar_one_or_none()

        if not user:
            continue

        education = await db.execute(
            select(Education).where(Education.name == t["education"])
        )

        education = education.scalar_one_or_none()

        if not education:
            raise Exception(f"Education {t['education']} not found")

        exists = await db.execute(
            select(Tutor).where(Tutor.user_id == user.id)
        )

        if exists.scalar_one_or_none():
            continue

        db.add(Tutor(
            user_id=user.id,
            bio=t["bio"],
            experience_years=2,
            education_id=education.id,
            price_per_hour=t["price"],
            currency="KZT",
            average_rating=t["average_rating"],
            total_reviews=t["total_reviews"],
        ))

    await db.commit()