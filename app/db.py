from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from .config import PG_HOST, PG_NAME, PG_PASS, PG_PORT, PG_USER


PG_URL: str = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_NAME}"
engine: AsyncEngine = create_async_engine(PG_URL, echo=True, future=True)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, ...]:
    async with async_session() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_session)]
