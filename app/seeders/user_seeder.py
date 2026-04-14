from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from data_access.db.models.user import User
from data_access.db.models.role import Role
from utils.password_hasher import hash_password


async def seed_users(db: AsyncSession):

    roles = (await db.execute(select(Role))).scalars().all()
    role_map = {r.name: r for r in roles}

    users = [
        ("Admin", "User", "admin@example.com", "admin123", "admin"),
        ("John", "Student", "john@example.com", "123", "student"),
        ("Jane", "Student", "jane@example.com", "123", "student"),
        ("Alice", "Tutor", "alice@example.com", "123", "tutor"),
        ("Bob", "Tutor", "bob@example.com", "123", "tutor"),
    ]

    for first, last, email, pwd, role in users:
        exists = await db.execute(select(User).where(User.email == email))
        if exists.scalar_one_or_none():
            continue

        db.add(User(
            first_name=first,
            last_name=last,
            email=email,
            password_hash=hash_password(pwd),
            role_id=role_map[role].id if role in role_map else None
        ))

    await db.commit()