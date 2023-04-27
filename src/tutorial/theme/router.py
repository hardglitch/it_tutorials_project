from typing import Annotated, List
from fastapi import APIRouter, Path
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, UserResponses
from src.db import DBSession
from src.tutorial.theme.crud import add_theme, delete_theme, edit_theme, get_all_themes, get_theme
from src.tutorial.theme.schemas import AddTutorialThemeScheme, EditTutorialThemeScheme, GetTutorialThemeScheme
from src.user.auth import Token, is_admin


Code = Annotated[int, Path(title="A Code of a Distribution Type")]

theme_router = APIRouter(prefix="/theme", tags=["tutorial theme"])


@theme_router.post("/add")
async def add_new_theme(request: Request, theme: AddTutorialThemeScheme, db_session: DBSession) -> str:
    if not all([request, theme, db_session]): return CommonResponses.FAILED

    token: Token = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await add_theme(theme, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@theme_router.put("/edit")
async def edit_existing_theme(request: Request, theme: EditTutorialThemeScheme, db_session: DBSession) -> str:
    if not all([request, theme, db_session]): return CommonResponses.FAILED

    token: Token = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await edit_theme(theme, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@theme_router.post("/del/{code}")
async def delete_existing_theme(request: Request, code: Code, db_session: DBSession) -> str:
    if not all([request, code, db_session]): return CommonResponses.FAILED

    token: Token = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await delete_theme(code, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@theme_router.get("/get/{code}")
async def get_existing_theme(code: Code, db_session: DBSession) -> GetTutorialThemeScheme:
    if not code or not db_session: return CommonResponses.FAILED
    theme = await get_theme(code, db_session)
    return theme if theme else CommonResponses.FAILED


@theme_router.get("/getall")
async def get_all_existing_themes(db_session: DBSession) -> List[GetTutorialThemeScheme]:
    if not db_session: return CommonResponses.FAILED
    themes = await get_all_themes(db_session)
    return themes if themes else CommonResponses.FAILED

