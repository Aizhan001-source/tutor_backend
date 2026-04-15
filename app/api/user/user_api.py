from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from api.user.user_schemas import (
    UserCreate,
    UserLogin,
    UserRead,
    UserProfileRead,
    UserUpdate
)

from business_logic.user.user_service import UserService
from data_access.db.session import get_db
from utils.auth_middleware import get_current_user


router = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("/register", response_model=UserRead)
async def register_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.register_user(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password=payload.password,
        avatar_url=getattr(payload, "avatar_url", None),
    )


# =========================
# LOGIN
# =========================
@router.post("/login")
async def login_user(
    payload: UserLogin,
    service: UserService = Depends(get_user_service),
):
    return await service.login_user(
        email=payload.email,
        password=payload.password,
    )


# =========================
# GET CURRENT USER PROFILE
# =========================
@router.get("/me", response_model=UserProfileRead)
async def get_my_profile(
    current_user=Depends(get_current_user()),
    service: UserService = Depends(get_user_service),
):
    return await service.get_user_profile(current_user.id)


# =========================
# UPDATE PROFILE
# =========================
@router.patch("/me", response_model=UserProfileRead)
async def update_my_profile(
    payload: UserUpdate,
    current_user=Depends(get_current_user()),
    service: UserService = Depends(get_user_service),
):
    return await service.update_user_profile(current_user.id, payload)


# =========================
# GET USER BY ID (ADMIN)
# =========================
@router.get("/{user_id}", response_model=UserProfileRead)
async def get_user_by_id(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.get_user_profile(user_id)


# =========================
# GET ALL USERS (ADMIN)
# =========================
@router.get("/", response_model=list[UserRead])
async def get_all_users(
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.repo.get_all_users()


# =========================
# DELETE USER (ADMIN)
# =========================
@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user(required_roles=["admin"])),
):
    user = await service.repo.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await service.repo.delete_user(user)

    return {"message": "User deleted successfully"}