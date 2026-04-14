from data_access.users.users_repository import UsersRepository
from data_access.db.models import User
from api.users.users_schemas import UserCreate
from core.password import hash_password, verify_password
from core.jwt import create_access_token


class UsersService:
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    async def get_users(self):
        return await self.repo.get_all()

    async def get_user_by_id(self, user_id: int):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    async def create_user(self, data: UserCreate):
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,   
            password_hash=hash_password(data.password),
        )

        return await self.repo.create(user)
    
    async def authenticate(self, email: str, password: str):
        user = await self.repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        token = create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "role_id": str(user.role_id)
        })

        return token