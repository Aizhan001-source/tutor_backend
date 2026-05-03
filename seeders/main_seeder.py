import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.session import AsyncSessionLocal

# import всех сидеров
from seeders.role_seeder import seed_roles
from seeders.user_seeder import seed_users
from seeders.education_seeder import seed_educations
from seeders.subject_seeder import seed_subjects
from seeders.tutor_seeder import seed_tutors
from seeders.student_seeder import seed_students
from seeders.courses_seeder import seed_courses
from seeders.schedule_seeder import seed_schedules
from seeders.booking_seeder import seed_bookings
from seeders.review_seeder import seed_reviews


async def run_seeders(db: AsyncSession):
    print("🚀 Seeding started...\n")

    # БАЗОВЫЕ СПРАВОЧНИКИ
    print("Seeding roles...")
    await seed_roles(db)

    print("Seeding educations...")
    await seed_educations(db)

    print("Seeding subjects...")
    await seed_subjects(db)

    # ПОЛЬЗОВАТЕЛИ
    print("Seeding users...")
    await seed_users(db)

    # ЗАВИСИМЫЕ СУЩНОСТИ
    print("Seeding tutors...")
    await seed_tutors(db)

    print("Seeding students...")
    await seed_students(db)

    # БИЗНЕС-СУЩНОСТИ
    print("Seeding courses...")
    await seed_courses(db)

    print("Seeding schedules...")
    await seed_schedules(db)

    print("Seeding bookings...")
    await seed_bookings(db)

    print("Seeding reviews...")
    await seed_reviews(db)

    print("\n✅ Seeding completed!")


async def main():
    async with AsyncSessionLocal() as db:
        try:
            await run_seeders(db)
        except Exception as e:
            await db.rollback()
            print(f"❌ Seeding failed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())