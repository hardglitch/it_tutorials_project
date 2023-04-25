from sqlalchemy import Result, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants.constants import Credential
from src.user.auth import get_hashed_password
from src.user.models import User
from src.user.schemas import AddUserScheme, EditUserScheme, GetUserScheme, UserIDScheme


async def add_user(user: AddUserScheme, async_session: AsyncSession) -> bool | None:
    async with async_session as session:
        try:
            if not user or not async_session: return False

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
            raise


async def edit_user(user_id: int, user_data: EditUserScheme, async_session: AsyncSession) -> bool | None:
    if not all([user_id, user_data, async_session]): return False

    async with async_session as session:
        try:
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
            return True

        except IntegrityError:
            raise


async def delete_user(user_id: int, async_session: AsyncSession) -> bool | None:
    """
    This function doesn't remove 'User' from the DB,
    it changes 'is_active' to False.
    """

    if not user_id or not async_session: return False

    async with async_session as session:
        try:
            await session.execute(
                update(User).where(User.id == user_id).values(is_active=False)
            )
            await session.commit()
            return True

        except IntegrityError:
            raise


async def get_user(user_id: int, async_session: AsyncSession) -> GetUserScheme | None:
    if not user_id or not async_session: return None

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

            return GetUserScheme(
                name=user_name,
                decoded_credential=Credential(user_credential).name,
                rating=user_rating,
            ) \
                if user_name and\
                   user_credential is not None and\
                   user_rating is not None and\
                   user_is_active\
                else None

        except IntegrityError:
            raise
