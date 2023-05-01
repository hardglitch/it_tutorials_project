from typing import List
from fastapi import APIRouter
from starlette.requests import Request
from app.common.responses import ResponseScheme
from app.db import DBSession
from app.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from app.tools import parameter_checker
from app.tutorial.type.crud import Code, add_tutorial_type, delete_tutorial_type, edit_tutorial_type, \
    get_all_tutorial_types, get_tutorial_type
from app.tutorial.type.schemas import GetTutorialTypeScheme
from app.user.auth import get_token_from_cookie, is_admin
from app.user.exceptions import UserExceptions

type_router = APIRouter(prefix="/type", tags=["tutorial type"])


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
