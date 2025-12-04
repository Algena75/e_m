import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import EmailStr
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    APP_TITLE: str = 'Сервис для управления пользователями'
    APP_DESCRIPTION: str = 'Тестовое задание'

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str | int = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    DATABASE_URL: str = (f"postgresql+asyncpg://{POSTGRES_USER}:"
                         f"{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:"
                         f"{POSTGRES_PORT}/{POSTGRES_DB}")
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'
        extra = 'allow'


settings = Settings()

LIFETIME = 3600
