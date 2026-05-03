from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.users.user_schemas import UserAdminCreate, UserCreate, UserLogin, UserRead
from utils.auth_middleware import get_current_user
from business_logic.users.user_service import UserService
from data_access.db.session import get_db
from api.users.user_schemas import CurrentUser

router = APIRouter()

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("/register", response_model=UserRead)
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

@router.get("/all")
async def get_all_users(
    service: UserService = Depends(get_user_service),
    user: CurrentUser = Depends(get_current_user),
):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    return await service.get_all_users()


@router.get("/profile")
async def get_user_profile(
    service: UserService = Depends(get_user_service),
    user: CurrentUser = Depends(get_current_user),
):
    result = await service.get_user_profile(user.id)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return result