from typing import Annotated, List
from fastapi import APIRouter
from starlette.requests import Request
from src.constants.exceptions import UserExceptions
from src.constants.responses import ResponseScheme
from src.db import DBSession
from src.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from src.tools import parameter_checker
from src.tutorial.type.crud import add_tutorial_type, delete_tutorial_type, edit_tutorial_type, get_all_tutorial_types, \
    get_tutorial_type
from src.tutorial.type.schemas import GetTutorialTypeScheme, TypeCodeScheme
from src.user.auth import get_token_from_cookie, is_admin


type_router = APIRouter(prefix="/type", tags=["tutorial type"])
Code = Annotated[int, TypeCodeScheme]


@type_router.post("/add")
@parameter_checker()
async def add_new_tutorial_type(request: Request, dist_type: AddWordToDictionaryScheme, db_session: DBSession) -> ResponseScheme:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await add_tutorial_type(dist_type, db_session)


@type_router.put("/edit")
@parameter_checker()
async def edit_existing_tutorial_type(request: Request, dist_type: EditDictionaryScheme, db_session: DBSession) -> ResponseScheme:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await edit_tutorial_type(dist_type, db_session)


@type_router.post("/del/{code}")
@parameter_checker()
async def delete_existing_tutorial_type(request: Request, code: Code, db_session: DBSession) -> ResponseScheme:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await delete_tutorial_type(code, db_session)


@type_router.get("/get/{code}")
@parameter_checker()
async def get_existing_tutorial_type(code: Code, db_session: DBSession) -> GetTutorialTypeScheme:
    return await get_tutorial_type(code, db_session)


@type_router.get("/getall")
@parameter_checker()
async def get_all_existing_tutorial_types(db_session: DBSession) -> List[GetTutorialTypeScheme]:
    return await get_all_tutorial_types(db_session)
