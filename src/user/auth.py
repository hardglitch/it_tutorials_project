from copy import deepcopy
from datetime import datetime, timedelta
from typing import Annotated, Dict
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Result, select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.config import SECRET_KEY
from src.db import get_session
from src.db_const import Credential
from src.exceptions import AuthenticateExceptions
from src.models import User
from src.user.schemas import UserCreateScheme, UserFullReadScheme, UserReadScheme, UserUpdateScheme
from src.responses import UserResponses


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes="bcrypt", deprecated="auto")


def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


async def create_user(user: UserCreateScheme, async_session: AsyncSession = Depends(get_session)) -> Dict[str, str]:
    async with async_session as session:
        try:
            new_user = User(
                name=user.name,
                email=user.email,
                hashed_password=get_hashed_password(user.password),
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return UserResponses.USER_CREATED
        except IntegrityError:
            return UserResponses.USER_ALREADY_EXISTS


async def authenticate_user(username: str, password: str,
                            async_session: AsyncSession = Depends(get_session)) -> User | None:
    async with async_session as session:
        try:
            result: Result = await session.execute(select(User).where(User.name == username))
            user: UserFullReadScheme | None = result.scalar_one_or_none()
            return None if not user or not verify_password(password, user.hashed_password) else user
        except HTTPException:
            raise
        except DBAPIError:
            raise


async def safe_get_user(user_id: int, async_session: AsyncSession = Depends(get_session)) -> User | None:
    async with async_session as session:
        try:
            result: Result = await session.execute(
                select(
                    User.name,
                    User.credential,
                    User.is_active,
                    User.rating,
                )
                .where(User.id == user_id)
            )
            res = result.fetchone()
            user: UserReadScheme | None = UserReadScheme(
                name=res[0],
                credential=res[1],
                is_active=res[2],
                rating=res[3]
            )
            return user
        except HTTPException:
            raise
        except DBAPIError:
            raise


async def get_user_data_before_update(
        user_id: int,
        async_session: AsyncSession = Depends(get_session)
) -> UserUpdateScheme | None:

    async with async_session as session:
        try:
            result: Result = await session.execute(
                select(
                    User.name,
                    User.email,
                    User.hashed_password,
                    User.credential
                )
                .where(User.id == user_id)
            )
            res = result.fetchone()
            return UserUpdateScheme(
                name=res[0],
                email=res[1],
                password=res[2],
                credential=res[3]
            )

        except HTTPException:
            raise
        except DBAPIError:
            raise


async def update_user(
        user_id: int,
        new_user_data: UserUpdateScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool:

    async with async_session as session:
        try:
            user = await session.get(User, user_id)
            user_snapshot = deepcopy(user)

            if user.name and new_user_data.name and user.name != new_user_data.name:
                user.name = new_user_data.name

            if user.email and new_user_data.email and user.email != new_user_data.email:
                user.email = new_user_data.email

            if new_user_data.password and user.hashed_password:
                new_hashed_password = get_hashed_password(new_user_data.password)
                if user.hashed_password != new_hashed_password:
                    user.hashed_password = new_hashed_password

            if user.credential == Credential.admin and new_user_data.credential\
                    and user.credential != new_user_data.credential:
                user.credential = new_user_data.credential

            if user.name != user_snapshot.name or \
               user.email != user_snapshot.email or \
               user.hashed_password != user_snapshot.hashed_password or \
               user.credential != user_snapshot.credential:

                session.add(user)
                await session.commit()
                await session.refresh(user)
                return True
            else:
                return False

        except HTTPException:
            raise
        except DBAPIError:
            raise


def create_access_token(user_name: str, user_id: int, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    claims = {
        "sub": user_name,
        "uid": user_id,
        "exp": datetime.utcnow() + expires_delta
    }
    return jwt.encode(claims=claims, key=SECRET_KEY, algorithm="HS256")


def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Dict[str, str]:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms="HS256")
        username = payload.get("sub")
        user_id = payload.get("uid")
        if not username or not user_id: raise AuthenticateExceptions.CREDENTIAL_EXCEPTION
        return {"username": username, "id": user_id}
    except JWTError:
        raise AuthenticateExceptions.CREDENTIAL_EXCEPTION


def validate_access(user_id: int, token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    try:
        user_id_from_token = decode_access_token(token)["id"]
        return user_id_from_token == user_id
    except Exception:
        return False
