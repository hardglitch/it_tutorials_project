from copy import deepcopy
from datetime import datetime, timedelta
from typing import Annotated, Dict
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Result, select, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.config import SECRET_KEY
from src.db import get_session
from src.constants.constants import AccessToken, Credential
from src.constants.exceptions import AuthenticateExceptions
from src.user.models import User
from src.user.schemas import UserCreateScheme, UserFullReadScheme, UserReadScheme, UserUpdateScheme

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes="bcrypt", deprecated="auto")


def get_hashed_password(password: str) -> str | None:
    if not all([
        password,
        isinstance(password, str)
    ]): return None
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not all([
        plain_password,
        hashed_password,
        isinstance(plain_password, str),
        isinstance(hashed_password, str)
    ]): return False
    return bcrypt_context.verify(plain_password, hashed_password)


async def create_user(
        user: UserCreateScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool:

    async with async_session as session:
        try:
            if not all([param is not None for param in user]): return False

            new_user = User(
                name=user.name,
                email=user.email,
                hashed_password=get_hashed_password(user.password),
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return True
        except IntegrityError:
            return False


async def authenticate_user(
        username: str,
        password: str,
        async_session: AsyncSession = Depends(get_session)
) -> UserFullReadScheme | None:

    async with async_session as session:
        try:
            result: Result = await session.execute(select(User).where(User.name == username))
            user: UserFullReadScheme | None = result.scalar_one_or_none()
            return None if not user or not verify_password(password, user.hashed_password) else user
        except HTTPException:
            raise
        except DBAPIError:
            raise


async def safe_get_user(
        user_id: int,
        async_session: AsyncSession = Depends(get_session)
) -> UserReadScheme | None:

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
            for row in result:
                user_name = row.name
                user_credential = row.credential
                user_is_active = row.is_active
                user_rating = row.rating

            return UserReadScheme(
                name=user_name,
                credential=user_credential,
                is_active=user_is_active,
                rating=user_rating,
            ) \
                if user_name and\
                   user_credential is not None and\
                   user_rating is not None and\
                   user_is_active is not None\
                else None

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
                if new_hashed_password and user.hashed_password != new_hashed_password:
                    user.hashed_password = new_hashed_password

            if user.credential and user.credential == Credential.admin and \
               new_user_data.credential and user.credential != new_user_data.credential:
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


async def delete_user_from_database(
        user_id: int,
        async_session: AsyncSession = Depends(get_session)
) -> bool:

    async with async_session as session:
        try:
            await session.execute(
                update(User).where(User.id == user_id).values(is_active=False)
            )
            await session.commit()
            return True

        except HTTPException:
            raise
        except DBAPIError:
            raise


async def is_admin(
        user_id_or_token: int | Annotated[str, Depends(oauth2_scheme)],
        async_session: AsyncSession
) -> bool:

    if not user_id_or_token: return False

    async with async_session as session:
        try:
            user_id = user_id_or_token if user_id_or_token.isnumeric() \
                else decode_access_token(user_id_or_token)[AccessToken.user_id]

            result: Result = await session.execute(select(User.credential).where(User.id == user_id))
            row = result.one()
            return True if row[0] == Credential.admin else False

        except Exception:
            return False


def create_access_token(
        user_name: str,
        user_id: int,
        expires_delta: timedelta = timedelta(minutes=AccessToken.expiration_time)
) -> str:
    claims = {
        AccessToken.subject: user_name,
        AccessToken.user_id: user_id,
        AccessToken.expired: datetime.utcnow() + expires_delta
    }
    return jwt.encode(claims=claims, key=SECRET_KEY, algorithm=AccessToken.algorithm)


def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Dict[str, str]:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=AccessToken.algorithm)
        user_name = payload.get(AccessToken.subject)
        user_id = payload.get(AccessToken.user_id)
        if not user_name or not user_id: raise AuthenticateExceptions.CREDENTIAL_EXCEPTION
        return {AccessToken.subject: user_name, AccessToken.user_id: user_id}
    except JWTError:
        raise AuthenticateExceptions.CREDENTIAL_EXCEPTION


def validate_access_token(user_id: int, token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    try:
        return user_id == decode_access_token(token)[AccessToken.user_id]
    except Exception:
        return False
