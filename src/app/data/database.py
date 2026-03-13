from collections.abc import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Base(DeclarativeBase):
    pass

DATABASE_URL = "sqlite+aiosqlite:///./ecomute.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session