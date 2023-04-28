from typing import Annotated, List
from fastapi import APIRouter, Path
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.exceptions import CommonExceptions, UserExceptions
from src.constants.responses import CommonResponses, ResponseScheme, UserResponses
from src.db import DBSession
from src.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from src.tutorial.type.crud import add_tutorial_type, delete_tutorial_type, edit_tutorial_type, get_all_tutorial_types, \
    get_tutorial_type
from src.tutorial.type.schemas import GetTutorialTypeScheme, TypeCodeScheme
from src.user.auth import Token, get_token_from_cookie, is_admin


type_router = APIRouter(prefix="/type", tags=["tutorial type"])
Code = Annotated[int, TypeCodeScheme]


@type_router.post("/add")
async def add_new_tutorial_type(
        request: Request,
        dist_type: AddWordToDictionaryScheme,
        db_session: DBSession
) -> ResponseScheme:

    try:
        if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
        return await add_tutorial_type(dist_type, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@type_router.put("/edit")
async def edit_existing_tutorial_type(
        request: Request,
        dist_type: EditDictionaryScheme,
        db_session: DBSession
) -> ResponseScheme:

    try:
        if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
        return await edit_tutorial_type(dist_type, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@type_router.post("/del/{code}")
async def delete_existing_tutorial_type(request: Request, code: Code, db_session: DBSession) -> ResponseScheme:
    try:
        if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
        return await delete_tutorial_type(code, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@type_router.get("/get/{code}")
async def get_existing_tutorial_type(code: Code, db_session: DBSession) -> GetTutorialTypeScheme:
    try:
        return await get_tutorial_type(code, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@type_router.get("/getall")
async def get_all_existing_tutorial_types(db_session: DBSession) -> List[GetTutorialTypeScheme]:
    try:
        return await get_all_tutorial_types(db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS
