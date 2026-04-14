from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from api.users.user_schemas import UserCreate, UserLogin, UserLoginResponse, UserRead, UserUpdate
from utils.auth_middleware import get_current_user
from data_access.users.user_repository import UserRepository
from business_logic.users.user_service import UserService
from data_access.db.session import get_db

router = APIRouter()

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

@router.post("/register", response_model=-UserRead)
async def user_register(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.register_user(user.first_name, user.last_name, user.email, user.password)


@router.post("/login")
async def user_login(
    user: UserLogin,
    service: UserService = Depends(get_user_service),
):
    result = await service.login_user(user.email, user.password)
    
    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return result


@router.put("/profile")
async def update_user_profile(
    user_profile: UserUpdate,
    service: UserService = Depends(get_user_service),
    user=Depends(get_current_user(required_roles=["admin, student, tutor"])),
):
    result = await service.update_user_profile(int("user_id"), user_profile)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result