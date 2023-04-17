from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.db import get_session
from src.constants.constants import Table, AccessToken
from src.models import Tutorial
from src.tutorial.crud import create_tutorial, decrypt_tutorial, get_tutorial_from_db
from src.tutorial.schemas import DecryptedTutorialScheme, TutorialScheme
from src.user.auth import decode_access_token, oauth2_scheme
from src.constants.responses import TutorialResponses


tutorial_router = APIRouter(prefix="/tutorial", tags=["tutorial"])


@tutorial_router.post("/add")
async def add_tutorial(
        request: Request,
        tutorial: TutorialScheme,
        async_session: AsyncSession = Depends(get_session)
):
    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    user = decode_access_token(token)
    return await create_tutorial(
        tutorial=tutorial,
        user_id=int(user[Table.User.id]),
        async_session=async_session
    )


@tutorial_router.post("/{tutorial_id}")
async def get_tutorial(tutorial_id: int, async_session: AsyncSession = Depends(get_session)) -> DecryptedTutorialScheme | str:
    tutor: Tutorial = await get_tutorial_from_db(tutorial_id=tutorial_id, async_session=async_session)
    return decrypt_tutorial(tutor) if tutor else TutorialResponses.TUTORIAL_NOT_FOUND
