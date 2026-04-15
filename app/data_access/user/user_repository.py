from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from sqlalchemy.orm import selectinload

from data_access.db.models.user import User
from data_access.db.models.role import Role


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------------------
    # CREATE USER
    # ---------------------------
    async def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        hashed_password: str,
        role_name: str = "student",
        avatar_url: str | None = None,
    ) -> User:

        # получаем роль
        result = await self.db.execute(
            select(Role).where(Role.name == role_name)
        )
        role = result.scalar_one_or_none()

        if not role:
            raise ValueError(f"Role '{role_name}' not found")

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hashed_password,
            role_id=role.id,
            avatar_url=avatar_url,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    # ---------------------------
    async def get_user_by_email(self, email: str):
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    # ---------------------------
    async def get_user_by_id(self, user_id: UUID):
        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.role))
        )
        return result.scalar_one_or_none()

    # ---------------------------
    async def get_all_users(self) -> list[User]:
        result = await self.db.execute(
            select(User).options(selectinload(User.role))
        )
        return result.scalars().all()

    # ---------------------------
    async def update_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # ---------------------------
    async def delete_user(self, user: User) -> bool:
        await self.db.delete(user)
        await self.db.commit()
        return True

    # ---------------------------
    async def get_user_role_by_user_id(self, user_id: UUID) -> str | None:
        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.role))
        )

        user = result.scalar_one_or_none()

        if not user or not user.role:
            return None

        return user.role.name