from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, Path
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Row, ScalarResult, and_, select
from starlette.requests import Request
from app.config import SECRET_KEY
from app.common.constants import AccessToken, Credential
from app.db import DBSession
from app.tools import db_checker, parameter_checker
from app.tutorial.models import TutorialModel
from app.tutorial.schemas import TutorialID
from app.user.exceptions import AuthenticateExceptions, UserExceptions
from app.user.schemas import Password, UserID, UserName, UserSchema
from app.user.models import UserModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes="bcrypt", deprecated="auto")

Token = Annotated[str, Depends(oauth2_scheme)]


@parameter_checker()
def get_hashed_password(password: str) -> str:
    return str(bcrypt_context.hash(password))


@db_checker()
async def authenticate_user(user_name: UserName, user_pwd: Password, db_session: DBSession) -> (int, str):
    result: ScalarResult = await db_session.scalars(select(UserModel).where(UserModel.name == user_name))
    user: UserModel | None = result.one_or_none()
    if not user or not bcrypt_context.verify(user_pwd.get_secret_value(), user.hashed_password):
        raise AuthenticateExceptions.INCORRECT_PARAMETERS
    return user.id, user.name


@db_checker()
async def is_this(credential: Credential, token: Token, db_session: DBSession) -> bool:
    user_data: UserSchema = decode_access_token(token)
    result: ScalarResult = await db_session.scalars(
        select(UserModel.credential)
        .where(and_(UserModel.id == user_data.id, UserModel.name == user_data.name, UserModel.is_active == True))
    )
    cred = result.one_or_none()
    if not cred: return False

    match credential:
        case Credential.user:
            if cred == Credential.user: return True
        case Credential.moderator:
            if cred == Credential.moderator: return True
        case Credential.admin:
            if cred == Credential.admin: return True
        case _:
            return False


@parameter_checker()
def is_me(user_id: UserID, request: Request) -> bool:
    return True if user_id == decode_access_token(get_token(request)).id else False


@parameter_checker()
async def is_admin(request: Request, db_session: DBSession) -> bool:
    if not await is_this(credential=Credential.admin, token=get_token(request), db_session=db_session):
        raise UserExceptions.ACCESS_DENIED
    return True


@parameter_checker()
async def is_tutorial_editor(
        tutor_id: Annotated[TutorialID, Path()],
        request: Request,
        db_session: DBSession
) -> TutorialID:

    token: Token = get_token(request)
    user_data: UserSchema = decode_access_token(token)

    result: ScalarResult = await db_session.scalars(
        select(
            UserModel.credential,
            TutorialModel.who_added_id
        )
        .where(and_(
            UserModel.id == user_data.id,
            UserModel.name == user_data.name,
            UserModel.is_active == True,
            TutorialModel.id == tutor_id
        ))
    )
    row: Row | None = result.one_or_none()
    if not row: raise UserExceptions.ACCESS_DENIED

    if not row.who_added_id == user_data.id and\
       not (row.credential == Credential.admin or row.credential == Credential.moderator):
        raise UserExceptions.ACCESS_DENIED
    return tutor_id


async def is_me_or_admin(user_id: UserID, request: Request, db_session: DBSession) -> bool:
    token: Token = get_token(request)
    if not user_id == decode_access_token(token).id and\
       not await is_this(credential=Credential.admin, token=token, db_session=db_session):
        raise UserExceptions.ACCESS_DENIED
    return True


def create_access_token(uid: UserID, name: UserName, exp_delta: int = AccessToken.exp_delta) -> str:
    try:
        claims = {
            AccessToken.subject: name,
            AccessToken.user_id: uid,
            AccessToken.expired: datetime.utcnow() + timedelta(seconds=exp_delta)
        }
        return str(jwt.encode(claims=claims, key=SECRET_KEY, algorithm=AccessToken.algorithm))

    except (JWTError, ValueError, TypeError):
        raise AuthenticateExceptions.FAILED_TO_CREATE_TOKEN


def decode_access_token(token: Token) -> UserSchema:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=AccessToken.algorithm)
        user_name = payload.get(AccessToken.subject)
        user_id = payload.get(AccessToken.user_id)
        if not user_name or not user_id: raise AuthenticateExceptions.FAILED_TO_DECODE_TOKEN
        return UserSchema(
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


