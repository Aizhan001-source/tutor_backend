from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.role import Role
from sqlalchemy import select

async def seed_roles(db: AsyncSession):
    roles = ["admin", "student", "tutor"]

    for role_name in roles:
        result = await db.execute(select(Role).where(Role.name == role_name))
        exists = result.scalar_one_or_none()
        if not exists:
            role = Role(name=role_name)
            db.add(role)

    await db.commit()
    print("Roles seeded!")