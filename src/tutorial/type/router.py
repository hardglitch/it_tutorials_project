from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, UserResponses
from src.db import get_session
from src.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from src.tutorial.type.crud import add_tutorial_type, delete_tutorial_type, edit_tutorial_type
from src.user.auth import is_admin, oauth2_scheme

type_router = APIRouter(prefix="/type", tags=["tutorial type"])


@type_router.post("/add")
async def add_new_tutorial_type(
        request: Request,
        dist_type: AddWordToDictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not all([request, dist_type, async_session]): return CommonResponses.FAILED

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await add_tutorial_type(dist_type, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@type_router.put("/edit")
async def edit_existing_tutorial_type(
        request: Request,
        dist_type: EditDictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not all([request, dist_type, async_session]): return CommonResponses.FAILED

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await edit_tutorial_type(dist_type, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@type_router.post("/del/{code}")
async def delete_existing_tutorial_type(
        request: Request,
        code: Annotated[int, Path(title="A Code of a Tutorial Type", ge=0)],
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not all([request, code, async_session]): return CommonResponses.FAILED

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await delete_tutorial_type(code, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED
