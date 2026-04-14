import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from data_access.db.models.role import Role
from data_access.db.models.user import User
from data_access.db.session import AsyncSessionLocal


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def seed_roles(db: AsyncSession):
    roles = ["admin", "manager", "user"]

    for role_name in roles:
        result = await db.execute(
            select(Role).where(Role.name == role_name)
        )
        role = result.scalar_one_or_none()

        if not role:
            db.add(Role(name=role_name))

    await db.commit()


async def seed_users(db: AsyncSession):
    admin_role = (
        await db.execute(select(Role).where(Role.name == "admin"))
    ).scalar_one_or_none()

    user_role = (
        await db.execute(select(Role).where(Role.name == "user"))
    ).scalar_one_or_none()

    if not admin_role or not user_role:
        raise Exception("Roles not found")

    users_data = [
        {
            "email": "admin@example.com",
            "password": "admin123",
            "first_name": "Admin",
            "last_name": "User",
            "role_id": admin_role.id,
        },
        {
            "email": "user@example.com",
            "password": "user123",
            "first_name": "Regular",
            "last_name": "User",
            "role_id": user_role.id,
        }
    ]

    for u in users_data:
        result = await db.execute(
            select(User).where(User.email == u["email"])
        )
        exists = result.scalar_one_or_none()

        if not exists:
            user = User(
                email=u["email"],
                password_hash=hash_password(u["password"]),
                first_name=u["first_name"],
                last_name=u["last_name"],
                role_id=u["role_id"],
                is_verified=True,
                is_active=True
            )
            db.add(user)

    await db.commit()


async def run_seeders(db: AsyncSession):
    await seed_roles(db)
    await seed_users(db)


async def main():
    async with AsyncSessionLocal() as db:
        await run_seeders(db)


if __name__ == "__main__":
    asyncio.run(main())