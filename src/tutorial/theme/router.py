from typing import Annotated, List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, UserResponses
from src.db import get_session
from src.tutorial.theme.crud import add_theme, delete_theme, edit_theme, get_all_themes, get_theme
from src.tutorial.theme.schemas import AddTutorialThemeScheme, EditTutorialThemeScheme, GetTutorialThemeScheme
from src.user.auth import is_admin, oauth2_scheme

theme_router = APIRouter(prefix="/theme", tags=["tutorial theme"])


@theme_router.post("/add")
async def add_new_theme(
        request: Request,
        theme: AddTutorialThemeScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not all([request, theme, async_session]): return CommonResponses.FAILED

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await add_theme(theme, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@theme_router.put("/edit")
async def edit_existing_theme(
        request: Request,
        theme: EditTutorialThemeScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not all([request, theme, async_session]): return CommonResponses.FAILED

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await edit_theme(theme, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@theme_router.post("/del/{code}")
async def delete_existing_theme(
        request: Request,
        code: Annotated[int, Path(title="A Code of a Distribution Type")],
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not all([request, code, async_session]): return CommonResponses.FAILED

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await delete_theme(code, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@theme_router.get("/get/{code}")
async def get_existing_theme(
        code: Annotated[int, Path(title="A Code of a Distribution Type")],
        async_session: AsyncSession = Depends(get_session)
) -> GetTutorialThemeScheme:

    if not code or not async_session: return CommonResponses.FAILED
    theme = await get_theme(code, async_session)
    return theme if theme else CommonResponses.FAILED


@theme_router.get("/getall")
async def get_all_existing_themes(async_session: AsyncSession = Depends(get_session)
) -> List[GetTutorialThemeScheme]:

    if not async_session: return CommonResponses.FAILED
    themes = await get_all_themes(async_session)
    return themes if themes else CommonResponses.FAILED

