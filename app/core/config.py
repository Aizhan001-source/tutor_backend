import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # app
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "tutor_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    @property
    def DATABASE_URL(self) -> str:
        # Используем asyncpg в строке подключения
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()