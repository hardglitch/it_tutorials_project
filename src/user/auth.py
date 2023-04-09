from datetime import datetime, timedelta
from typing import Dict
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import SECRET_KEY
from src.db import get_session
from src.models import User
from src.user.schemas import UserFullRead
from src.exceptions import AuthenticateExceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes="bcrypt", deprecated="auto")


def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str, async_session: AsyncSession = Depends(get_session)) -> User | None:
    async with async_session as session:
        try:
            result: Result = await session.execute(select(User).where(User.name == username))
            user: UserFullRead | None = result.scalar_one_or_none()
            return None if not user or not verify_password(password, user.hashed_password) else user
        except HTTPException:
            raise


def create_access_token(user_name: str, user_id: int, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    claims = {
        "sub": user_name,
        "uid": user_id,
        "exp": datetime.utcnow() + expires_delta
    }
    return jwt.encode(claims=claims, key=SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms="HS256")
        username = payload.get("sub")
        user_id = payload.get("uid")
        if not username or not user_id: raise AuthenticateExceptions.CredentialsException
        return {"username": username, "id": user_id}
    except JWTError:
        raise AuthenticateExceptions.CredentialsException
