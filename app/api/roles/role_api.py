from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth_middleware import get_current_user
from business_logic.roles.role_service import RoleService
from data_access.db.session import get_db

router = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)) -> RoleService:
    return RoleService(db)


@router.get("/all")
async def get_all_users(
    service: RoleService = Depends(get_user_service),
    user=Depends(get_current_user),
):
    result = await service.get_all_roles()
    
    return result