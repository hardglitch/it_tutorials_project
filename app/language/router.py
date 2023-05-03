from typing import List
from fastapi import APIRouter
from starlette.requests import Request
from app.common.responses import ResponseSchema
from app.db import DBSession
from app.language.crud import LangCode, add_language, delete_language, edit_language, get_all_languages, get_language
from app.language.schemas import EditLanguageSchema, LanguageSchema
from app.tools import parameter_checker
from app.user.auth import get_token, is_admin
from app.user.exceptions import UserExceptions


language_router = APIRouter(prefix="/lang", tags=["language"])


@language_router.post("/add")
@parameter_checker()
async def add_new_language(request: Request, lang: LanguageSchema, db_session: DBSession) -> ResponseSchema:
    if not await is_admin(request, db_session): raise UserExceptions.ACCESS_DENIED
    return await add_language(lang, db_session)


@language_router.put("/edit")
@parameter_checker()
async def edit_existing_language(request: Request, lang: EditLanguageSchema, db_session: DBSession) -> ResponseSchema:
    if not await is_admin(get_token(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await edit_language(lang, db_session)


@language_router.delete("/del/{lang_code}")
@parameter_checker()
async def delete_existing_language(request: Request, lang_code: LangCode, db_session: DBSession) -> ResponseSchema:
    if not await is_admin(get_token(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await delete_language(lang_code, db_session)


@parameter_checker()
@language_router.get("/get/{lang_code}")
async def get_existing_language(lang_code: LangCode, db_session: DBSession) -> LanguageSchema:
    return await get_language(lang_code, db_session)


@language_router.get("/get-all")
@parameter_checker()
async def get_all_existing_languages(db_session: DBSession) -> List[EditLanguageSchema]:
    return await get_all_languages(db_session)
