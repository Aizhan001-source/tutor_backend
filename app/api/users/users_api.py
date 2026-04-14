from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.users_schemas import UserCreate, TokenResponse, LoginSchema, UserRead
from data_access.db.session import get_db
from data_access.users.users_repository import UsersRepository
from business_logic.users.users_service import UsersService

router = APIRouter()


def get_users_service(db: AsyncSession = Depends(get_db)) -> UsersService:
    repo = UsersRepository(db)
    return UsersService(repo)


@router.post("/register", response_model=UserRead)
async def register(
    data: UserCreate, 
    service: UsersService = Depends(get_users_service)):
    return await service.create_user(data)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginSchema, service: UsersService = Depends(get_users_service)):
    try:
        token = await service.authenticate(data.email, data.password)
        return {"access_token": token}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
