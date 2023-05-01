from typing import List
from sqlalchemy import Result, Row, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.constants import Credential
from app.common.exceptions import CommonExceptions
from app.common.responses import CommonResponses, ResponseScheme
from app.tools import db_checker
from app.user.auth import UserID, get_hashed_password
from app.user.models import User
from app.user.schemas import AddUserScheme, EditUserScheme, GetUserScheme


@db_checker()
async def add_user(user: AddUserScheme, db_session: AsyncSession) -> GetUserScheme:
    async with db_session as session:
        new_user = User(
            name=user.name,
            email=user.email,
            hashed_password=get_hashed_password(user.password),
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return GetUserScheme(
            id=new_user.id,
            name=new_user.name,
            decoded_credential=Credential(new_user.credential).name,
            rating=new_user.rating
        )


@db_checker()
async def edit_user(user_id: UserID, user_data: EditUserScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                name=user_data.name,
                email=user_data.email,
                hashed_password=get_hashed_password(user_data.password)
            )
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def delete_user(user_id: UserID, db_session: AsyncSession) -> ResponseScheme:
    """
    This function doesn't remove 'User' from the DB,
    it changes 'is_active' to False.
    """
    async with db_session as session:
        await session.execute(
            update(User).where(User.id == user_id).values(is_active=False)
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def get_user(user_id: UserID, db_session: AsyncSession) -> GetUserScheme:
    async with db_session as session:
        result: Result = await session.execute(
            select(
                User.id,
                User.name,
                User.credential,
                User.is_active,
                User.rating,
            )
            .where(User.id == user_id)
        )

        user: Row = result.one_or_none()
        if not user or not user.is_active: raise CommonExceptions.NOTHING_FOUND
        return GetUserScheme(
            id=user.id,
            name=user.name,
            decoded_credential=Credential(user.credential).name,
            rating=user.rating,
        )


@db_checker()
async def get_all_users(db_session: AsyncSession) -> List[GetUserScheme]:
    async with db_session as session:
        result: Result = await session.execute(
            select(
                User.id,
                User.name,
                User.credential,
                User.is_active,
                User.rating,
            )
            .order_by(User.id)
        )

        users: List[GetUserScheme] = []
        for user in result.all():
            if not user.is_active: continue
            users.append(
                GetUserScheme(
                    id=user.id,
                    name=user.name,
                    decoded_credential=Credential(user.credential).name,
                    rating=user.rating,
                )
            )
        if not users: raise CommonExceptions.NOTHING_FOUND
        return users
