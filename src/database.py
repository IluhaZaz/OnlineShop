from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

meta_data = MetaData()

from config import db_settings as stngs


DATABASE_URL = f"postgresql+asyncpg://{stngs.DB_USER}:{stngs.DB_PASS}@{stngs.DB_HOST}:{stngs.DB_PORT}/{stngs.DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
