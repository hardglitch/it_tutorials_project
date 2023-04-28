from typing import Annotated, List
from fastapi import APIRouter, Path
from starlette.requests import Request
from src.constants.exceptions import CommonExceptions, UserExceptions
from src.constants.responses import ResponseScheme
from src.db import DBSession
from src.language.crud import add_language, delete_language, edit_language, get_all_languages, get_language
from src.language.schemas import EditLanguageScheme, LanguageScheme
from src.user.auth import get_token_from_cookie, is_admin


language_router = APIRouter(prefix="/lang", tags=["language"])
LangCode = Annotated[int, Path(title="Language Code", ge=0)]


@language_router.post("/add")
async def add_new_language(request: Request, lang: LanguageScheme, db_session: DBSession) -> int:
    try:
        if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
        return await add_language(lang, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@language_router.put("/edit")
async def edit_existing_language(request: Request, lang: EditLanguageScheme, db_session: DBSession) -> ResponseScheme:
    try:
        if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
        return await edit_language(lang, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@language_router.delete("/del/{lang_code}")
async def delete_existing_language(request: Request, lang_code: LangCode, db_session: DBSession) -> ResponseScheme:
    try:
        if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
        return await delete_language(lang_code, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@language_router.get("/get/{lang_code}")
async def get_existing_language(lang_code: LangCode, db_session: DBSession) -> LanguageScheme:
    try:
        return await get_language(lang_code, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@language_router.get("/getall")
async def get_all_existing_languages(db_session: DBSession) -> List[LanguageScheme]:
    try:
        return await get_all_languages(db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS
