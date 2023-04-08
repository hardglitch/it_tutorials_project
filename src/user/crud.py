from typing import Dict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.user.models import User
from src.user.schemas import UserCreate


async def get_user(user_id: int, async_session: AsyncSession = Depends(get_session)) -> User | None:
    async with async_session as session:
        # async with session.begin():
        try:
            result = await session.get(User, user_id)
            # result = await session.execute(select(User).filter(User.id == user_id))
            # res = result.scalars().first()
            await session.commit()
            return result
        except Exception:
            raise


async def create_user(user: UserCreate, async_session: AsyncSession = Depends(get_session)) -> Dict[str, str]:
    async with async_session as session:
        try:
            new_user = User(
                name=user.name,
                email=user.email,
                hashed_password=hash(user.password),   # TODO: make a normal hash function
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return {"response": "OK"}
        except Exception:
            raise

