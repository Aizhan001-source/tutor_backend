from fastapi import Depends, HTTPException
from api.users.user_schemas import UserProfileRead, UserRead
from errors.user_error import UserAlreadyExistsError
from data_access.users.user_repository import UserRepository
import hashlib
from utils.token_creator import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register_user(self, first_name, last_name, email, password):
        try:
            created_user = await self.repo.register_user(
                first_name,
                last_name,
                email,
                self.__hash_password(password),
            )
        except UserAlreadyExistsError:
            raise HTTPException(
                status_code=409,
                detail="User with this email already exists"
            )

        return UserRead(
            id=created_user.id,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            email=created_user.email,
            role=created_user.role.name,
        )

    async def login_user(self, email, password):
        hashed_password = self.__hash_password(password)
        
        logged_in_user = await self.repo.login_user(email, hashed_password)
        
        print("QWEQWEQWEQW: ")

        if not logged_in_user:
            return None  

        token_data = {"sub": str(logged_in_user.id), "email": logged_in_user.email}
        access_token = create_access_token(token_data)

        print("LOGGED IN USER: ", logged_in_user.role)

        return {
            "user": UserRead(
                id=logged_in_user.id,
                first_name=logged_in_user.first_name,
                last_name=logged_in_user.last_name,
                email=logged_in_user.email,
                role=logged_in_user.role.name,
            ),
            "access_token": access_token,
            "token_type": "bearer"
        }

    def __hash_password(self, password: str) -> str:
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    async def get_user_role_by_user_id(self, user_id) -> str:
        return await self.repo.get_user_role_by_user_id(user_id)

    async def get_user_profile(self, user_id):
        user = await self.repo.get_user_profile(user_id)

        if not user:
            return None

        return UserProfileRead(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )

    async def update_user_profile(self, user_id, user_profile):
        user = await self.repo.get_user_profile(user_id)

        if not user:
            return None

        if user_profile.first_name is not None:
            user.first_name = user_profile.first_name

        if user_profile.last_name is not None:
            user.last_name = user_profile.last_name
        if user_profile.email is not None:

            user.email = user_profile.email
        
        if user_profile.new_password is not None and user_profile.old_password is not None:
            print("QWEQWEBQWHJQEJQEQBEBHWJL: ", user_profile.old_password, user_profile.new_password)
            
            if self.__hash_password(user_profile.old_password) != user.password:
                raise HTTPException(status_code=400, detail="Old password is incorrect")
            user.password = self.__hash_password(user_profile.new_password)

        await self.repo.update_user_profile(user)

        return UserProfileRead(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )