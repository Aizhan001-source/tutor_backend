from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from data_access.db.models.role import Role
from data_access.db.models.user import User
from errors.user_error import UserAlreadyExistsError


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, first_name, last_name, email, hashed_password, role_name: str):
        result = await self.db.execute(
            select(Role).where(Role.name == role_name)
        )
        role = result.scalar_one_or_none()

        if not role:
            raise Exception(f"Role '{role_name}' not found")

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hashed_password,
            role_id=role.id
        )

        self.db.add(user)

        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user

        except IntegrityError:
            await self.db.rollback()
            raise UserAlreadyExistsError("User already exists")

    async def get_by_email(self, email: str):
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_profile(self, user_id: UUID):
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_user_profile(self, user: User):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user