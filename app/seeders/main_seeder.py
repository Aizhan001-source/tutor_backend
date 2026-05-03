import asyncio, sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_access.db.session import AsyncSessionLocal
from role_seeder import seed_roles
from user_seeder import seed_users
from booking_seeder import seed_bookings
from payment_seeder import seed_payments
from favorite_seeder import seed_favorites
from tutor_seeder import seed_tutors
from education_seeder import seed_educations


async def main():
    async with AsyncSessionLocal() as db:

        # 1. базовые справочники
        await seed_roles(db)
        await seed_educations(db)

        # 2. пользователи (students + tutors users)
        await seed_users(db)

        # 3. tutors (зависит от users + educations)
        await seed_tutors(db)

        # 4. bookings (зависит от students + tutors)
        await seed_bookings(db)

        # 5. payments (зависит от bookings)
        await seed_payments(db)

        # 6. favorites (зависит от students + tutors)
        await seed_favorites(db)

if __name__ == "__main__":
    asyncio.run(main())