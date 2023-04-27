from typing import Annotated
from fastapi import APIRouter, Path
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, UserResponses
from src.db import DBSession
from src.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from src.tutorial.dist_type.crud import add_distribution_type, delete_distribution_type, edit_distribution_type
from src.user.auth import Token, is_admin

dist_type_router = APIRouter(prefix="/dist_type", tags=["tutorial distribution type"])


@dist_type_router.post("/add")
async def add_new_distribution_type(
        request: Request,
        dist_type: AddWordToDictionaryScheme,
        db_session: DBSession
) -> str:

    if not all([request, dist_type, db_session]): return CommonResponses.FAILED

    token: Token = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await add_distribution_type(dist_type, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@dist_type_router.put("/edit")
async def edit_existing_distribution_type(
        request: Request,
        dist_type: EditDictionaryScheme,
        db_session: DBSession
) -> str:

    if not all([request, dist_type, db_session]): return CommonResponses.FAILED

    token: Token = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await edit_distribution_type(dist_type, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@dist_type_router.post("/del/{code}")
async def delete_existing_distribution_type(
        request: Request,
        code: Annotated[int, Path(title="A Code of a Distribution Type", ge=0)],
        db_session: DBSession
) -> str:

    if not all([request, code, db_session]): return CommonResponses.FAILED

    token: Token = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await delete_distribution_type(code, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED
