from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Result, Row, ScalarResult, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from app.config import SECRET_KEY
from app.common.constants import AccessToken, Credential
from app.tools import db_checker, parameter_checker
from app.user.exceptions import AuthenticateExceptions, UserExceptions
from app.user.models import User
from app.user.schemas import AuthUserSchema, PasswordSchema, UserIDSchema, UserNameSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes="bcrypt", deprecated="auto")

Token = Annotated[str, Depends(oauth2_scheme)]
UserID = Annotated[int, UserIDSchema]
UserName = Annotated[str, UserNameSchema]
UserPassword = Annotated[str, PasswordSchema]


@parameter_checker()
def get_hashed_password(password: UserPassword) -> str:
    return str(bcrypt_context.hash(password))


@db_checker()
async def authenticate_user(user_name: UserName, password: UserPassword, db_session: AsyncSession) -> AuthUserSchema:
    async with db_session as session:
        result: ScalarResult = await session.scalars(select(User).where(User.name == user_name))
        user: User | None = result.one_or_none()
        if not user or not bcrypt_context.verify(password, user.hashed_password):
            raise AuthenticateExceptions.INCORRECT_PARAMETERS
        return AuthUserSchema(
            id=user.id,
            name=user.name
        )


@db_checker()
async def is_this(credential: Credential, token: Token, db_session: AsyncSession) -> bool:
    async with db_session as session:
        user_data: AuthUserSchema = decode_access_token(token)
        result: Result = await session.execute(
            select(User)
            .where(and_(User.id == user_data.id, User.name == user_data.name, User.is_active is True))
        )
        user: Row | None = result.one_or_none()
        if not user: return False

        match credential:
            case Credential.user:
                if user.credential == Credential.user: return True
            case Credential.moderator:
                if user.credential == Credential.moderator: return True
            case Credential.admin:
                if user.credential == Credential.admin: return True
            case _:
                return False


@parameter_checker()
def is_me(user_id: UserID, request: Request) -> bool:
    if user_id == decode_access_token(get_token(request)).id: return True
    raise UserExceptions.ACCESS_DENIED


@parameter_checker()
async def is_admin(request: Request, db_session: AsyncSession) -> bool:
    if not await is_this(Credential.admin, get_token(request), db_session): return True
    raise UserExceptions.ACCESS_DENIED


def create_access_token(token_data: AuthUserSchema, exp_delta: int = AccessToken.exp_delta) -> str:
    try:
        claims = {
            AccessToken.subject: token_data.name,
            AccessToken.user_id: token_data.id,
            AccessToken.expired: datetime.utcnow() + timedelta(seconds=exp_delta)
        }
        return str(jwt.encode(claims=claims, key=SECRET_KEY, algorithm=AccessToken.algorithm))

    except (JWTError, ValueError, TypeError):
        raise AuthenticateExceptions.FAILED_TO_CREATE_TOKEN


def decode_access_token(token: Token) -> AuthUserSchema:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=AccessToken.algorithm)
        user_name = payload.get(AccessToken.subject)
        user_id = payload.get(AccessToken.user_id)
        if not user_name or not user_id: raise AuthenticateExceptions.FAILED_TO_DECODE_TOKEN
        return AuthUserSchema(
            name=user_name,
            id=user_id
        )
    except ExpiredSignatureError:
        raise AuthenticateExceptions.TOKEN_EXPIRED
    except (JWTError, ValueError, TypeError):
        raise AuthenticateExceptions.FAILED_TO_DECODE_TOKEN


def get_token(request: Request) -> Token:
    try:
        return Token(request.cookies.get(AccessToken.name))
    except (TypeError, ValueError):
        raise AuthenticateExceptions.TOKEN_NOT_FOUND
