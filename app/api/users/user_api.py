from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.user_schemas import (
    UserCreate,
    UserLogin,
    UserLoginResponse,
    UserRead,
    UserUpdate,
)
from utils.auth_middleware import get_current_user
from business_logic.users.user_service import UserService
from data_access.db.session import get_db

router = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


# ✅ REGISTER
@router.post("/register", response_model=UserRead)
async def user_register(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.register_user(
        user.first_name,
        user.last_name,
        user.email,
        user.password
    )


# ✅ LOGIN
@router.post("/login", response_model=UserLoginResponse)
async def user_login(
    user: UserLogin,
    service: UserService = Depends(get_user_service),
):
    return await service.login_user(user.email, user.password)


# ✅ UPDATE PROFILE
@router.put("/profile", response_model=UserRead)
async def update_user_profile(
    user_profile: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user=Depends(
        get_current_user(required_roles=["admin", "student", "tutor"])
    ),
):
    return await service.update_user_profile(
        current_user.id,
        user_profile
    )