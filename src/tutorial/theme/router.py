from typing import List
from fastapi import APIRouter
from starlette.requests import Request
from src.constants.exceptions import UserExceptions
from src.constants.responses import ResponseScheme
from src.db import DBSession
from src.tools import parameter_checker
from src.tutorial.theme.crud import Code, add_theme, delete_theme, edit_theme, get_all_themes, get_theme
from src.tutorial.theme.schemas import AddTutorialThemeScheme, EditTutorialThemeScheme, GetTutorialThemeScheme
from src.user.auth import get_token_from_cookie, is_admin


theme_router = APIRouter(prefix="/theme", tags=["tutorial theme"])


@theme_router.post("/add")
@parameter_checker()
async def add_new_theme(request: Request, theme: AddTutorialThemeScheme, db_session: DBSession) -> ResponseScheme:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await add_theme(theme, db_session)


@theme_router.put("/edit")
@parameter_checker()
async def edit_existing_theme(request: Request, theme: EditTutorialThemeScheme, db_session: DBSession) -> ResponseScheme:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await edit_theme(theme, db_session)


@theme_router.post("/del/{code}")
@parameter_checker()
async def delete_existing_theme(request: Request, code: Code, db_session: DBSession) -> ResponseScheme:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await delete_theme(code, db_session)


@theme_router.get("/get/{code}")
@parameter_checker()
async def get_existing_theme(code: Code, db_session: DBSession) -> GetTutorialThemeScheme:
    return await get_theme(code, db_session)


@theme_router.get("/getall")
@parameter_checker()
async def get_all_existing_themes(db_session: DBSession) -> List[GetTutorialThemeScheme]:
    return await get_all_themes(db_session)
