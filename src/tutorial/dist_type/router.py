from typing import Annotated, List
from fastapi import APIRouter, Path
from starlette.requests import Request
from src.constants.exceptions import CommonExceptions, UserExceptions
from src.constants.responses import ResponseScheme
from src.db import DBSession
from src.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from src.tutorial.dist_type.crud import add_distribution_type, delete_distribution_type, edit_distribution_type, \
    get_all_distribution_types, get_distribution_type
from src.tutorial.dist_type.schemas import GetTutorialDistributionTypeScheme
from src.user.auth import get_token_from_cookie, is_admin


dist_type_router = APIRouter(prefix="/dist_type", tags=["tutorial distribution type"])
Code = Annotated[int, Path(title="A Code of a Distribution Type", ge=0)]


@dist_type_router.post("/add")
async def add_new_distribution_type(request: Request, dist_type: AddWordToDictionaryScheme, db_session: DBSession):
    try:
        if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
        return await add_distribution_type(dist_type, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@dist_type_router.put("/edit")
async def edit_existing_distribution_type(request: Request, dist_type: EditDictionaryScheme, db_session: DBSession) -> ResponseScheme:
    try:
        if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
        return await edit_distribution_type(dist_type, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@dist_type_router.post("/del/{code}")
async def delete_existing_distribution_type(request: Request, code: Code, db_session: DBSession) -> ResponseScheme:
    try:
        if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
        return await delete_distribution_type(code, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@dist_type_router.get("/get/{code}")
async def get_existing_distribution_type(code: Code, db_session: DBSession) -> GetTutorialDistributionTypeScheme:
    try:
        return await get_distribution_type(code, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@dist_type_router.get("/getall")
async def get_all_existing_distribution_types(db_session: DBSession) -> List[GetTutorialDistributionTypeScheme]:
    try:
        return await get_all_distribution_types(db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS

