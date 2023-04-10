from datetime import timedelta
from typing import Dict
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.user.schemas import UserCreate
from src.user.auth import authenticate_user, create_access_token, create_user
from src.exceptions import AuthenticateExceptions
from src.responses import UserResponses


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/registration")
async def user_registration(user: UserCreate, async_session: AsyncSession = Depends(get_session)):
    resp = await create_user(user=user, async_session=async_session)
    return UserResponses.USER_CREATED if resp is True else resp


@user_router.post("/login")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        async_session: AsyncSession = Depends(get_session)
    ) -> Dict[str, str]:
    user = await authenticate_user(form_data.username, form_data.password, async_session)
    if not user: raise AuthenticateExceptions.TOKEN_EXCEPTION
    return {
        "token": create_access_token(user_name=user.name, user_id=user.id, expires_delta=timedelta(minutes=20))
    }


# @user_router.post("/get")
# async def get_user(user_id: int, async_session: AsyncSession = Depends(get_session)) -> User | None:
#     async with async_session as session:
#         try:
#             result = await session.get(User, user_id)
#             # result = await session.execute(select(User).filter(User.id == user_id))
#             # res = result.scalars().first()
#             await session.commit()
#             return result
#         except Exception:
#             raise
