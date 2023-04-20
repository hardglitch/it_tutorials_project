from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, LanguageResponses, UserResponses
from src.db import get_session
from src.language.crud import add_language, edit_language
from src.language.schemas import EditLanguageScheme, LanguageScheme
from src.user.auth import is_admin, oauth2_scheme

language_router = APIRouter(prefix="/lang", tags=["language"])


@language_router.post("/add")
async def add_new_language(
        request: Request,
        lang: LanguageScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if is_admin(token, async_session):
        return CommonResponses.SUCCESS if await add_language(lang, async_session) \
            else LanguageResponses.FAILED_TO_ADD_LANGUAGE
    else:
        return UserResponses.ACCESS_DENIED


@language_router.patch("/edit")
async def edit_existing_language(
        request: Request,
        lang: EditLanguageScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if is_admin(token, async_session):
        return CommonResponses.SUCCESS if await edit_language(lang, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED
