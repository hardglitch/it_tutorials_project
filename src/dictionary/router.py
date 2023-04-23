from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, UserResponses
from src.db import get_session
from src.dictionary.crud import add_word, edit_word
from src.dictionary.schemas import DictionaryScheme
from src.user.auth import is_admin, oauth2_scheme

dictionary_router = APIRouter(prefix="/dict", tags=["dictionary"])


@dictionary_router.post("/add")
async def add_new_word_to_dictionary(
        request: Request,
        word: DictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await add_word(word, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@dictionary_router.patch("/edit")
async def edit_existing_word(
        request: Request,
        word: DictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await edit_word(word, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED
