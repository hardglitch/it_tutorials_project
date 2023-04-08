from typing import Dict
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.user.models import User
from src.user.schemas import UserCreate
from src.user.auth import authenticate_user, get_hashed_password


user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@user_router.post("/create")
async def create_user(user: UserCreate, async_session: AsyncSession = Depends(get_session)) -> Dict[str, str]:
    async with async_session as session:
        try:
            new_user = User(
                name=user.name,
                email=user.email,
                hashed_password=get_hashed_password(user.password),
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return {"response": "OK"}                     # TODO: Response
        except Exception:
            raise                                         # TODO: Exception



@user_router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        async_session: AsyncSession = Depends(get_session)
    ):
    return {"response": "User not found"} \
        if not await authenticate_user(form_data.username, form_data.password, async_session) \
        else {"response": "User validate"}



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
