import asyncio, sys
from pathlib import Path

# Добавляем корень проекта в sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_access.db.session import AsyncSessionLocal
from user_seeder import seed_users
from role_seeder import seed_roles
from education_seeder import seed_educations
from tutor_seeder import seed_tutors


async def main():
    async with AsyncSessionLocal() as db:
        # await seed_roles(db)
        # await seed_users(db)
        await seed_educations(db)
        await seed_tutors(db)


if __name__ == "__main__":
    asyncio.run(main())