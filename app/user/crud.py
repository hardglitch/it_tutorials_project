from typing import List
from sqlalchemy import Result, Row, select, update
from .exceptions import UserExceptions
from ..common.constants import DecodedCredential
from ..common.exceptions import CommonExceptions
from ..db import DBSession
from ..tools import db_checker
from ..user.auth import Credential, get_hashed_password
from ..user.schemas import IsActive, UserSchema, UserID
from ..user.models import UserModel


@db_checker()
async def add_user(user: UserSchema, db_session: DBSession, is_admin: bool = False) -> bool:
    new_user = UserModel(
        name=user.name,
        email=user.email,
        hashed_password=get_hashed_password(user.password.get_secret_value()),
    )
    if is_admin: new_user.credential = Credential.admin

    db_session.add(new_user)
    await db_session.commit()
    return True


@db_checker()
async def edit_user(user: UserSchema, db_session: DBSession) -> bool:
    await db_session.execute(
        update(UserModel)
        .where(UserModel.id == user.id)
        .values(
            name=user.name,
            email=user.email,
            hashed_password=get_hashed_password(user.password.get_secret_value())
        )
    )
    await db_session.commit()
    return True


@db_checker()
async def update_user_status(
        user_id: UserID,
        is_active: IsActive,
        credential: Credential,
        db_session: DBSession
) -> bool:

    await db_session.execute(
        update(UserModel)
        .where(UserModel.id == user_id)
        .values(
            is_active=is_active,
            credential=credential,
        )
    )
    await db_session.commit()
    return True


@db_checker()
async def delete_user(user_id: UserID, db_session: DBSession) -> bool:
    """
    This function doesn't remove 'User' from the DB,
    it changes 'is_active' to False.
    """
    await db_session.execute(
        update(UserModel).where(UserModel.id == user_id, UserModel.is_active == True).values(is_active=False)
    )
    await db_session.commit()
    return True


@db_checker()
async def get_user(user_id: UserID, db_session: DBSession, is_me: bool = False, safe_mode: bool = False) -> UserSchema:
    result: Result = await db_session.execute(
        select(
            UserModel.id,
            UserModel.name,
            UserModel.email,
            UserModel.credential,
            UserModel.is_active,
            UserModel.rating,
        )
        .where(UserModel.id == user_id)
    )

    usr: Row = result.one()
    if not usr: raise CommonExceptions.NOTHING_FOUND
    if not usr.is_active and not safe_mode: raise UserExceptions.USER_HAS_BEEN_DELETED
    return UserSchema(
        id=usr.id,
        name=usr.name,
        email=usr.email if is_me else None,
        decoded_credential=DecodedCredential(Credential(usr.credential).name),
        rating=usr.rating,
        is_active=usr.is_active
    )


@db_checker()
async def get_all_users(db_session: DBSession) -> List[UserSchema]:
    result: Result = await db_session.execute(
        select(
            UserModel.id,
            UserModel.name,
            UserModel.credential,
            UserModel.is_active,
            UserModel.rating,
        )
        .order_by(UserModel.id)
    )

    users: List[UserSchema] = []
    for usr in result.all():
        # if not usr.is_active: continue
        users.append(
            UserSchema(
                id=usr.id,
                name=usr.name,
                credential=usr.credential,
                decoded_credential=DecodedCredential(Credential(usr.credential).name),
                rating=usr.rating,
                is_active=usr.is_active,
            )
        )
    if not users: raise CommonExceptions.NOTHING_FOUND
    return users
