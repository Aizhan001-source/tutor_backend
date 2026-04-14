from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from data_access.db.models.admin import Admin


class AdminRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Admin]:
        result = await self.db.execute(select(Admin))
        return result.scalars().all()
    

    async def get_by_id(self, admin_id: str) -> Admin | None:
        result = await self.db.execute(select(Admin).where(Admin.id == admin_id))
        return result.scalar_one_or_none()
    
    async def create(self, admin: Admin) -> Admin:
        self.db.add(admin)
        await self.db.commit()
        await self.db.refresh(admin)
        return admin