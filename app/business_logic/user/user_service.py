from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
import hashlib
import traceback

from data_access.user.user_repository import UserRepository
from utils.token_creator import create_access_token


class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)
        self.db = db

    async def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        avatar_url=None
    ):
        hashed_password = self.__hash_password(password)

        existing_user = await self.repo.get_user_by_email(email)
        if existing_user:
            raise HTTPException(409, "Email already registered")

        try:
            user = await self.repo.register_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                hashed_password=hashed_password,
                role_name="student",
                avatar_url=avatar_url
            )
            return user

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(409, "Database constraint violation")

        except Exception:
            await self.db.rollback()
            print(traceback.format_exc())
            raise HTTPException(500, "Internal error")

    async def login_user(self, email: str, password: str):
        user = await self.repo.get_user_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        hashed_password = self.__hash_password(password)

        if user.password_hash != hashed_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token({"sub": str(user.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    def __hash_password(self, password: str) -> str:
        return hashlib.md5(password.encode()).hexdigest()