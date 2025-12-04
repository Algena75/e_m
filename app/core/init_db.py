import contextlib
import os

import asyncpg
from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.models import User
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
        email: EmailStr, password: str,  firstname: str, is_superuser: bool = False
) -> User:
    """Создаёт и возвращет экземпляр пользователя."""
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user_created = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            firstname=firstname
                        )
                    )
                    return user_created
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """Создаёт первого суперпользователя при запуске проекта."""
    if (settings.first_superuser_email is not None and
            settings.first_superuser_password is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            firstname='Admin',
            is_superuser=True,
        )


async def create_db_if_not_exists():
    """Создаём БД, если не существует."""
    try:
        connection = await asyncpg.connect(
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            database=settings.POSTGRES_DB,
            password=settings.POSTGRES_PASSWORD
        )
        print(f'Подключено! Необходимая БД {settings.POSTGRES_DB} обнаружена')
        await connection.close()
        return
    except:
        connection = await asyncpg.connect(
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            user='postgres',
            database='template1',
            password='postgres'
        )
        CREATE_USER_IF_NOT_EXISTS = f"""
        DO
        $do$
        BEGIN
           IF EXISTS (
              SELECT FROM pg_catalog.pg_roles
              WHERE  rolname = '{settings.POSTGRES_USER}') THEN
              RAISE NOTICE 'Role "{settings.POSTGRES_USER}" is already exists. Skipping.';
           ELSE
              CREATE ROLE {settings.POSTGRES_USER} WITH LOGIN SUPERUSER
                PASSWORD '{settings.POSTGRES_PASSWORD}';
           END IF;
        END
        $do$;"""
        await connection.execute(CREATE_USER_IF_NOT_EXISTS)
        print('Пользователь создан!')
        CREATE_DB = f"""
        CREATE DATABASE {settings.POSTGRES_DB}
        OWNER '{settings.POSTGRES_USER}';
        """
        await connection.execute(CREATE_DB)
        print('База создана!')
        await connection.close()
        os.system('alembic upgrade head')
        await create_db_if_not_exists()
