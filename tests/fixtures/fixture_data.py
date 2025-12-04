import asyncpg
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.db import Base, get_async_session
from app.core.user import current_superuser, current_user
from app.main import app
from app.schemas.user import UserCreate

authenticated_user = UserCreate(
    email="user@example.com",
    firstname="Admin",
    password="qwerty",
    is_superuser=False
)
super_user = UserCreate(
    email="superuser@example.com",
    firstname="Superuser",
    password="qwerty",
    is_superuser=True
)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope='session')
async def async_db_engine():
    SQLALCHEMY_DATABASE_URL = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/test_base"
    )

    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    try:
        await create_database_if_not_exists()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield engine
    finally:
        print('SESSION IS CLOSED')
        await delete_database()


@pytest.fixture(scope='session')
async def async_db(async_db_engine):
    testing_session_local = sessionmaker(async_db_engine, class_=AsyncSession,
                                         expire_on_commit=False)
    async with testing_session_local() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(app=app,
                           base_url="http://localhost") as client:
        if app.dependency_overrides.get(current_user):
            del app.dependency_overrides[current_user]
        yield client


@pytest.fixture(scope='session')
async def authenticated_client(client, async_db: AsyncSession):
    app.dependency_overrides[current_user] = lambda: authenticated_user
    app.dependency_overrides[get_async_session] = lambda: async_db
    return client


@pytest.fixture(scope='session')
async def superuser_client(authenticated_client, async_db: AsyncSession):
    app.dependency_overrides[current_superuser] = lambda: super_user
    app.dependency_overrides[get_async_session] = lambda: async_db
    return client


async def create_database_if_not_exists():
    try:
        db_conn = await asyncpg.connect(user='postgres',
                                        password='postgres',
                                        database='template1',
                                        host='127.0.0.1')
        await db_conn.execute(f'''CREATE DATABASE test_base''')
        await db_conn.close()
    except:
        pass


async def delete_database():
    try:
        db_conn = await asyncpg.connect(user='postgres',
                                        password='postgres',
                                        database='template1',
                                        host='127.0.0.1')
        await db_conn.execute(f'''DROP DATABASE test_base WITH (FORCE)''')
        await db_conn.close()
    except:
        pass
