from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,  # sql logs
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async session"""
    try:
        async with async_session_maker() as session:
            yield session
    finally:
        if session:
            await session.close()
