from fastapi import Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.user.models import User

oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes="bcrypt", deprecated="auto")


def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str, async_session: AsyncSession = Depends(get_session)) -> bool:
    async with async_session as session:
        try:
            result: Result = await session.execute(select(User.hashed_password).where(User.name == username))
            hashed_password: str | None = result.scalar_one_or_none()
            return False if not hashed_password or not verify_password(password, hashed_password) else True
        except Exception:
            raise
