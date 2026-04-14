from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from data_access.db.models.role import Role
from data_access.db.models.user import User
from errors.user_error import UserAlreadyExistsError


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, first_name, last_name, email, hashed_password):
        result = await self.db.execute(
            select(Role).where(
                (Role.name == "tutor")
            )
        )
        role_object = result.scalar_one_or_none()
        
        user = User(
            first_name = first_name, 
            last_name = last_name, 
            email = email, 
            password_hash = hashed_password,
            role_id=role_object.id,
        )

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def login_user(self, email: str, hashed_password: str):
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(
                User.email == email,
                User.password_hash == hashed_password
            )
        )
        return result.scalar_one_or_none()


    async def get_user_role_by_user_id(self, user_id: int) -> str | None:
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
        )

        user = result.scalar_one_or_none()

        if user and user.role:
            return user.role.name
        return None


    async def get_user_Profile(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
        )

        user = result.scalar_one_or_none()

        return user
    

    async def update_user_profile(self, user: User):
        await self.db.commit()
        await self.db.refresh(user)
        return user