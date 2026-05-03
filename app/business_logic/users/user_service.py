from fastapi import Depends, HTTPException
from api.users.user_schemas import UserAllRead, UserLoginResponse, UserProfileRead, UserRead
from data_access.db.session import get_db
from data_access.users.user_repository import UserRepository
from uuid import UUID
from utils.token_creator import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from utils.password_hasher import hash_password
from utils.password_hasher import verify_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register_user(self, first_name, last_name, email, password):
        created_user = await self.repo.register_user(first_name, last_name, email, hash_password(password))

        return UserRead(
            id=created_user.id,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            email=created_user.email,
        )


    from utils.password_hasher import verify_password

    async def login_user(self, email, password):
        user = await self.repo.get_by_email(email)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        token = create_access_token({
            "sub": str(user.id),
            "email": user.email
        })

        return {
            "user": UserRead(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            ),
            "access_token": token,
            "token_type": "bearer"
        }

    async def get_all_users(self):
        all_users = await self.repo.get_all_users()
        
        return [
            UserAllRead.model_validate(user)
            for user in all_users
        ]

    async def get_user_role_by_user_id(self, user_id) -> str:
        return await self.repo.get_user_role_by_user_id(user_id)
    
    async def get_user_profile(self, user_id):
        user = await self.repo.get_user_profile(user_id)
        
        if not user:
            return None
        
        return UserProfileRead(
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
        )