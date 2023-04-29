from typing import Annotated
from sqlalchemy import Result, Row, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.constants import Credential
from src.constants.exceptions import CommonExceptions
from src.constants.responses import CommonResponses, ResponseScheme
from src.tools import parameter_checker
from src.user.auth import get_hashed_password
from src.user.models import User
from src.user.schemas import AddUserScheme, EditUserScheme, GetUserScheme, UserIDScheme


UserID = Annotated[int, UserIDScheme]


@parameter_checker()
async def add_user(user: AddUserScheme, db_session: AsyncSession) -> GetUserScheme:
    try:
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
                name=new_user.name,
                decoded_credential=Credential(new_user.credential).name,
                rating=new_user.rating
            )

    except IntegrityError:
        raise CommonExceptions.DUPLICATED_ENTRY


@parameter_checker()
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


@parameter_checker()
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


@parameter_checker()
async def get_user(user_id: UserID, db_session: AsyncSession) -> GetUserScheme:
    async with db_session as session:
        result: Result = await session.execute(
            select(
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
            name=user.name,
            decoded_credential=Credential(user.credential).name,
            rating=user.rating,
        )
