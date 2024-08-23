import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from database import get_async_session

from src.config import db_test_settings as s
from src.main import app
from auth.models import meta_data
from goods.models import meta_data


# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{s.DB_USER_TEST}:{s.DB_PASS_TEST}@{s.DB_HOST_TEST}:{s.DB_PORT_TEST}/{s.DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(meta_data.drop_all)
        await conn.run_sync(meta_data.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(meta_data.drop_all)

# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session')
def client():
    cl = TestClient(app)
    yield cl

@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac