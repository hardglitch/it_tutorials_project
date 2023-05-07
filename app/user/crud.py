from typing import List
from sqlalchemy import Result, Row, select, update
from ..common.constants import DecodedCredential
from ..common.exceptions import CommonExceptions
from ..common.responses import CommonResponses, ResponseSchema
from ..db import DBSession
from ..tools import db_checker
from ..user.auth import Credential, get_hashed_password
from ..user.schemas import UserSchema, UserID
from ..user.models import UserModel


@db_checker()
async def add_user(user: UserSchema, db_session: DBSession) -> UserSchema:
    new_user = UserModel(
        name=user.name,
        email=user.email,
        hashed_password=get_hashed_password(user.password.get_secret_value()),
    )

    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    return UserSchema(
        id=new_user.id,
        name=new_user.name,
        decoded_credential=DecodedCredential(Credential(new_user.credential).name),
        rating=new_user.rating
    )


@db_checker()
async def edit_user(user: UserSchema, db_session: DBSession) -> ResponseSchema:
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
    return CommonResponses.SUCCESS


@db_checker()
async def delete_user(user_id: UserID, db_session: DBSession) -> ResponseSchema:
    """
    This function doesn't remove 'User' from the DB,
    it changes 'is_active' to False.
    """
    await db_session.execute(
        update(UserModel).where(UserModel.id == user_id).values(is_active=False)
    )
    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def get_user(user_id: UserID, db_session: DBSession) -> UserSchema:
    result: Result = await db_session.execute(
        select(
            UserModel.id,
            UserModel.name,
            UserModel.credential,
            UserModel.is_active,
            UserModel.rating,
        )
        .where(UserModel.id == user_id)
    )

    usr: Row = result.one()
    if not usr or not usr.is_active: raise CommonExceptions.NOTHING_FOUND
    return UserSchema(
        id=usr.id,
        name=usr.name,
        decoded_credential=DecodedCredential(Credential(usr.credential).name),
        rating=usr.rating,
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
        if not usr.is_active: continue
        users.append(
            UserSchema(
                id=usr.id,
                name=usr.name,
                decoded_credential=DecodedCredential(Credential(usr.credential).name),
                rating=usr.rating,
            )
        )
    if not users: raise CommonExceptions.NOTHING_FOUND
    return users
