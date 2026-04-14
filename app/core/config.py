import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastApi App"
    DEBUG: bool = True
    HOST: str = "172.0.0.1"
    PORT: int = 8000

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str 
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    class Config:
        env_file = ".env"
        case_sensitive = True
        
settings = Settings()