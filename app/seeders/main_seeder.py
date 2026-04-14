import asyncio, sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_access.db.session import AsyncSessionLocal
from role_seeder import seed_roles
from user_seeder import seed_users
from payment_seeder import seed_payments
from booking_seeder import seed_bookings
from tutor_seeder import seed_tutors
from review_seeder import seed_reviews
from subject_seeder import seed_subjects


async def main():
    async with AsyncSessionLocal() as db:
        await seed_roles(db)
        await seed_subjects(db)
        await seed_users(db)
        await seed_tutors(db)
        await seed_bookings(db)
        await seed_payments(db)
        await seed_reviews(db)

        # await seed_favorites(db)
        # await seed_messages(db)

if __name__ == "__main__":
    asyncio.run(main())