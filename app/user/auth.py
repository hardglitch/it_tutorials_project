from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from app.config import SECRET_KEY
from app.common.constants import AccessToken, Credential
from app.tools import parameter_checker
from app.user.exceptions import AuthenticateExceptions
from app.user.models import User
from app.user.schemas import AuthUserScheme, PasswordScheme, UserIDScheme, UserNameScheme


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes="bcrypt", deprecated="auto")

Token = Annotated[str, Depends(oauth2_scheme)]
UserID = Annotated[int, UserIDScheme]
UserName = Annotated[str, UserNameScheme]
UserPassword = Annotated[str, PasswordScheme]


@parameter_checker()
def get_hashed_password(password: UserPassword) -> str:
    return str(bcrypt_context.hash(password))


@parameter_checker()
async def authenticate_user(user_name: UserName, password: UserPassword, db_session: AsyncSession) -> AuthUserScheme:
    async with db_session as session:
        result: ScalarResult = await session.scalars(select(User).where(User.name == user_name))
        user_data: User | None = result.one_or_none()
        if not user_data: raise AuthenticateExceptions.INCORRECT_PARAMETERS
        if not bcrypt_context.verify(password, user_data.hashed_password):
            raise AuthenticateExceptions.INCORRECT_PARAMETERS
        return AuthUserScheme(
            id=user_data.id,
            name=user_data.name
        )


async def is_admin(token: Token, db_session: AsyncSession) -> bool:
    try:
        async with db_session as session:
            user_id: int = decode_access_token(token).id
            result: ScalarResult = await session.scalars(select(User.credential).where(User.id == user_id))
            credential: int | None = result.one_or_none()
            return True if credential and credential == Credential.admin else False
    except Exception:
        return False


def create_access_token(token_data: AuthUserScheme, exp_delta: int = AccessToken.exp_delta) -> str:
    try:
        claims = {
            AccessToken.subject: token_data.name,
            AccessToken.user_id: token_data.id,
            AccessToken.expired: datetime.utcnow() + timedelta(seconds=exp_delta)
        }
        return str(jwt.encode(claims=claims, key=SECRET_KEY, algorithm=AccessToken.algorithm))

    except (JWTError, ValueError, TypeError):
        raise AuthenticateExceptions.FAILED_TO_CREATE_TOKEN


def decode_access_token(token: Token) -> AuthUserScheme:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=AccessToken.algorithm)
        user_name = payload.get(AccessToken.subject)
        user_id = payload.get(AccessToken.user_id)
        if not user_name or not user_id: raise AuthenticateExceptions.FAILED_TO_DECODE_TOKEN
        return AuthUserScheme(
            name=user_name,
            id=user_id
        )
    except ExpiredSignatureError:
        raise AuthenticateExceptions.TOKEN_EXPIRED
    except (JWTError, ValueError, TypeError):
        raise AuthenticateExceptions.FAILED_TO_DECODE_TOKEN


def get_token_from_cookie(request: Request) -> Token:
    try:
        return Token(request.cookies.get(AccessToken.name))
    except (TypeError, ValueError):
        raise AuthenticateExceptions.TOKEN_NOT_FOUND


@parameter_checker()
async def check_credential(user_id: UserID, token: Token, db_session: AsyncSession) -> bool:
    return True if user_id == decode_access_token(token).id or is_admin(token, db_session) else False
