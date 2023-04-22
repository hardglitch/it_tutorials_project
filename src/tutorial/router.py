from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.db import get_session
from src.constants.constants import AccessToken
from src.dictionary.models import Tutorial
from src.tutorial.crud import create_tutorial, get_tutorial_from_db
from src.tutorial.dist_type.router import dist_router
from src.tutorial.schemas import DecryptedTutorialScheme, TutorialScheme
from src.user.auth import decode_access_token, oauth2_scheme
from src.constants.responses import UserResponses


tutorial_router = APIRouter(prefix="/tutorial", tags=["tutorial"])
tutorial_router.include_router(dist_router)


@tutorial_router.post("/add")
async def add_tutorial(
        request: Request,
        tutorial: TutorialScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if not token: return UserResponses.ACCESS_DENIED

    tutorial.who_added_id = int(decode_access_token(token)[AccessToken.user_id])
    return await create_tutorial(tutorial, async_session)


@tutorial_router.post("/{tutorial_id}")
async def get_tutorial(
        tutorial_id: Annotated[int, Path(title="Tutorial ID")],
        async_session: AsyncSession = Depends(get_session)
) -> DecryptedTutorialScheme | str:

    tutor: Tutorial = await get_tutorial_from_db(tutorial_id, async_session)
    # return decrypt_tutorial(tutor) if tutor else TutorialResponses.TUTORIAL_NOT_FOUND
    pass

