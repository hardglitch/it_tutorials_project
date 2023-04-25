from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, UserResponses
from src.db import get_session
from src.dictionary.schemas import DictionaryScheme
from src.tutorial.dist_type.crud import add_distribution_type, delete_distribution_type, edit_distribution_type
from src.user.auth import is_admin, oauth2_scheme

dist_type_router = APIRouter(prefix="/dist_type", tags=["tutorial distribution type"])


@dist_type_router.post("/add")
async def add_new_distribution_type(
        request: Request,
        dist_type: DictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not all([request, dist_type, async_session]): return CommonResponses.FAILED

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await add_distribution_type(dist_type, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@dist_type_router.patch("/edit")
async def edit_existing_distribution_type(
        request: Request,
        dist_type: DictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not all([request, dist_type, async_session]): return CommonResponses.FAILED

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await edit_distribution_type(dist_type, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@dist_type_router.post("/del/{code}")
async def delete_existing_distribution_type(
        request: Request,
        code: Annotated[int, Path(title="A Code of a Distribution Type")],
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not all([request, code, async_session]): return CommonResponses.FAILED

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await delete_distribution_type(code, async_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED
