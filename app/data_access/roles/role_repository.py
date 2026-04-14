from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data_access.db.models.role import Role


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_roles(self):
        result = await self.db.execute(
            select(Role)
        )

        roles = result.scalars().all()
        return roles