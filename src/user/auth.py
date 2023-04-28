from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Result, ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request

from src.config import SECRET_KEY
from src.constants.constants import AccessToken, Credential
from src.constants.exceptions import AuthenticateExceptions, CommonExceptions
from src.user.models import User
from src.user.schemas import AccessTokenScheme, AuthUserScheme

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes="bcrypt", deprecated="auto")

Token = Annotated[str, Depends(oauth2_scheme)]


def get_hashed_password(password: str) -> str | None:
    try:
        return bcrypt_context.hash(password)
    except (TypeError, ValueError):
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt_context.verify(plain_password, hashed_password)
    except Exception:
        return False


async def authenticate_user(username: str, password: str, db_session: AsyncSession) -> AuthUserScheme | None:
    async with db_session as session:
        try:
            result: ScalarResult = await session.scalars(select(User).where(User.name == username))
            user_data: AuthUserScheme | None = result.one_or_none()
            if not user_data: raise CommonExceptions.NOTHING_FOUND
            return user_data if user_data and verify_password(password, user_data.hashed_password) else None

        except (TypeError, ValueError):
            raise CommonExceptions.INVALID_PARAMETERS


async def is_admin(user_id_or_token: int | Token, db_session: AsyncSession) -> bool:
    async with db_session as session:
        try:
            user_id: int = user_id_or_token if user_id_or_token.isnumeric() \
                else decode_access_token(user_id_or_token).id

            result: ScalarResult = await session.scalars(select(User.credential).where(User.id == user_id))
            credential: int | None = result.one_or_none()
            return True if credential and credential == Credential.admin else False

        except Exception:
            return False


def create_access_token(token_data: AccessTokenScheme, exp_delta: int = AccessToken.exp_delta) -> str:
    try:
        claims = {
            AccessToken.subject: token_data.name,
            AccessToken.user_id: token_data.id,
            AccessToken.expired: datetime.utcnow() + timedelta(seconds=exp_delta)
        }
        return jwt.encode(claims=claims, key=SECRET_KEY, algorithm=AccessToken.algorithm)

    except (JWTError, ValueError, TypeError):
        raise AuthenticateExceptions.FAILED_TO_CREATE_TOKEN


def decode_access_token(token: Token) -> AccessTokenScheme:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=AccessToken.algorithm)
        return AccessTokenScheme(
            name=payload.get(AccessToken.subject),
            id=payload.get(AccessToken.user_id)
        )

    except ExpiredSignatureError:
        raise AuthenticateExceptions.TOKEN_EXPIRED
    except (JWTError, ValueError, TypeError):
        raise AuthenticateExceptions.CREDENTIAL_EXCEPTION


def validate_access_token(user_id: int, token: Token) -> bool:
    try:
        return user_id == decode_access_token(token).id
    except Exception:
        return False


def get_token_from_cookie(request: Request) -> Token:
    try:
        return Token(request.cookies.get(AccessToken.name))
    except (TypeError, ValueError):
        raise AuthenticateExceptions.TOKEN_NOT_FOUND
