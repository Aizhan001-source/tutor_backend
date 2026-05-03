from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.password_hasher import hash_password
from data_access.db.models.user import User
from data_access.db.models.role import Role


async def seed_users(db: AsyncSession):
    # 1. Load roles
    result = await db.execute(select(Role))
    roles_list = result.scalars().all()

    roles = {role.name: role for role in roles_list}

    required_roles = ["admin", "student", "tutor"]

    # 2. Validate roles exist
    missing_roles = [r for r in required_roles if r not in roles]
    if missing_roles:
        raise Exception(f"Missing roles in DB: {missing_roles}")

    # 3. Users seed data
    users_data = [
        {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "password": "admin123",
            "role": "admin"
        },
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "student123",
            "role": "student"
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "janesmith@example.com",
            "password": "student123",
            "role": "student"
        },
        {
            "first_name": "Alice",
            "last_name": "Brown",
            "email": "alice@example.com",
            "password": "tutor123",
            "role": "tutor"
        },
        {
            "first_name": "Bob",
            "last_name": "White",
            "email": "bob@example.com",
            "password": "tutor123",
            "role": "tutor"
        }
    ]

    # 4. Insert users
    for u in users_data:
        # check exists
        result = await db.execute(
            select(User).where(User.email == u["email"])
        )
        exists = result.scalar_one_or_none()

        if exists:
            continue

        role = roles.get(u["role"])
        if not role:
            raise Exception(f"Role '{u['role']}' not found")

        user = User(
            first_name=u["first_name"],
            last_name=u["last_name"],
            email=u["email"],
            password_hash=hash_password(u["password"]),
            role_id=role.id
        )

        db.add(user)

    await db.commit()
    print("Users seeded successfully!")