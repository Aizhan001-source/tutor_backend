from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from business_logic.users.user_service import UserService
from data_access.db.session import get_db
from utils.token_creator import decode_access_token
from api.users.user_schemas import CurrentUser

security = HTTPBearer()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
) -> CurrentUser:
    try:
        payload = decode_access_token(credentials.credentials)
    except Exception:
        raise HTTPException(401, "Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(401, "Invalid token payload")

    user_id = UUID(user_id)

    role_name = await user_service.get_user_role_by_user_id(user_id)

    if not role_name:
        raise HTTPException(401, "User not found")

    return CurrentUser(
        id=user_id,
        role=role_name
    )