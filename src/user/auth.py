from datetime import datetime, timedelta
from typing import Annotated, Dict
from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Result, ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.config import SECRET_KEY
from src.constants.constants import AccessToken, Credential
from src.constants.exceptions import AuthenticateExceptions
from src.user.models import User
from src.user.schemas import AuthUserScheme

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes="bcrypt", deprecated="auto")

# aliases
Token = Annotated[str, Depends(oauth2_scheme)]


def get_hashed_password(password: str) -> str | None:
    if not all([password, isinstance(password, str)]): return None
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not all([plain_password, hashed_password, isinstance(plain_password, str), isinstance(hashed_password, str)]):
        return False
    return bcrypt_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str, async_session: AsyncSession) -> AuthUserScheme | None:
    async with async_session as session:
        try:
            result: Result = await session.execute(select(User).where(User.name == username))
            user_data: AuthUserScheme | None = result.scalar_one_or_none()
            return user_data if user_data and verify_password(password, user_data.hashed_password) else None

        except IntegrityError:
            raise


async def is_admin(
        user_id_or_token: int | Token,
        async_session: AsyncSession
) -> bool:

    if not user_id_or_token or not async_session: return False

    async with async_session as session:
        try:
            user_id: str = user_id_or_token if user_id_or_token.isnumeric() \
                else decode_access_token(user_id_or_token)[AccessToken.user_id]

            result: ScalarResult = await session.scalars(select(User.credential).where(User.id == user_id))
            credential: int = result.one()
            return True if credential == Credential.admin else False

        except Exception:
            return False


def create_access_token(
        user_name: str,
        user_id: int,
        exp_time: timedelta = timedelta(seconds=AccessToken.expiration_time)
) -> str:
    claims = {
        AccessToken.subject: user_name,
        AccessToken.user_id: user_id,
        AccessToken.expired: datetime.utcnow() + exp_time
    }
    return jwt.encode(claims=claims, key=SECRET_KEY, algorithm=AccessToken.algorithm)


def decode_access_token(token: Token) -> Dict[str, str]:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=AccessToken.algorithm)
        user_name = payload.get(AccessToken.subject)
        user_id = payload.get(AccessToken.user_id)
        if not user_name or not user_id: raise AuthenticateExceptions.CREDENTIAL_EXCEPTION
        return {AccessToken.subject: user_name, AccessToken.user_id: user_id}
    except JWTError:
        raise AuthenticateExceptions.CREDENTIAL_EXCEPTION


def validate_access_token(user_id: int, token: Token) -> bool:
    try:
        return user_id == decode_access_token(token)[AccessToken.user_id]
    except Exception:
        return False
