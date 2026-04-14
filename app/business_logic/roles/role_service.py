from api.roles.role_schemas import RoleRead
from data_access.roles.role_repository import RoleRepository
from sqlalchemy.ext.asyncio import AsyncSession

class RoleService:
    def __init__(self, db: AsyncSession):
        self.repo = RoleRepository(db)

    async def get_all_roles(self):
        all_roles = await self.repo.get_all_roles()
        
        return [
            RoleRead.model_validate(role)
            for role in all_roles
        ]