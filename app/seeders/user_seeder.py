from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from utils.password_hasher import hash_password
from data_access.db.models.user import User
from data_access.db.models.role import Role


async def seed_users(db: AsyncSession):
    # Берем роли из БД
    roles_result = await db.execute(select(Role))
    roles = {role.name: role for role in roles_result.scalars().all()}

    users_data = [
        {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "password": "admin123",
            "role": "admin"
        },
        {
            "first_name": "Jan",
            "last_name": "Dau",
            "email": "johndoe@example.com",
            "password": "reader123",
            "role": "student"
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "janesmith@example.com",
            "password": "reader123",
            "role": "student"
        },
        {
            "first_name": "Alice",
            "last_name": "Brown",
            "email": "alice@example.com",
            "password": "user123",
            "role": "tutor"
        },
        {
            "first_name": "Bob",
            "last_name": "White",
            "email": "bob@example.com",
            "password": "user123",
            "role": "tutor"
        }
    ]

    for u in users_data:
        # Проверка, есть ли пользователь с таким email
        result = await db.execute(select(User).where(User.email == u["email"]))
        exists = result.scalar_one_or_none()
        if not exists:
            user = User(
                first_name=u["first_name"],
                last_name=u["last_name"],
                email=u["email"],
                password_hash=hash_password(u["password"]),
                role_id=roles[u["role"]].id if u["role"] in roles else None
            )
            db.add(user)

    await db.commit()
    print("Users seeded!")