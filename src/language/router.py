from typing import Annotated
from fastapi import APIRouter, Depends, Path
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, LanguageResponses, UserResponses
from src.db import DBSession
from src.language.crud import add_language, delete_language, edit_language
from src.language.schemas import EditLanguageScheme, LanguageScheme
from src.user.auth import is_admin, oauth2_scheme

language_router = APIRouter(prefix="/lang", tags=["language"])


@language_router.post("/add")
async def add_new_language(
        request: Request,
        lang: LanguageScheme,
        db_session: DBSession
) -> str:

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await add_language(lang, db_session) \
            else LanguageResponses.FAILED_TO_ADD_LANGUAGE
    else:
        return UserResponses.ACCESS_DENIED


@language_router.patch("/edit")
async def edit_existing_language(
        request: Request,
        lang: EditLanguageScheme,
        db_session: DBSession
) -> str:

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await edit_language(lang, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@language_router.delete("/{lang_code}")
async def delete_existing_language(
        request: Request,
        lang_code: Annotated[int, Path(title="Language Code")],
        db_session: DBSession
) -> str:

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await delete_language(lang_code, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED
