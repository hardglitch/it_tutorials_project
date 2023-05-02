from typing import List
from fastapi import APIRouter
from starlette.requests import Request
from app.common.responses import ResponseSchema
from app.db import DBSession
from app.dictionary.schemas import AddWordToDictionarySchema, EditDictionarySchema
from app.tools import parameter_checker
from app.tutorial.dist_type.crud import Code, add_distribution_type, delete_distribution_type, edit_distribution_type, \
    get_all_distribution_types, get_distribution_type
from app.tutorial.dist_type.schemas import GetTutorialDistTypeSchema
from app.user.auth import get_token_from_cookie, is_admin
from app.user.exceptions import UserExceptions


dist_type_router = APIRouter(prefix="/dist-type", tags=["tutorial distribution type"])


@dist_type_router.post("/add")
@parameter_checker()
async def add_new_distribution_type(request: Request, dist_type: AddWordToDictionarySchema, db_session: DBSession) -> ResponseSchema:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await add_distribution_type(dist_type, db_session)


@dist_type_router.put("/edit")
@parameter_checker()
async def edit_existing_distribution_type(request: Request, dist_type: EditDictionarySchema, db_session: DBSession) -> ResponseSchema:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await edit_distribution_type(dist_type, db_session)


@dist_type_router.post("/del/{code}")
@parameter_checker()
async def delete_existing_distribution_type(request: Request, code: Code, db_session: DBSession) -> ResponseSchema:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await delete_distribution_type(code, db_session)


@dist_type_router.get("/get/{code}")
@parameter_checker()
async def get_existing_distribution_type(code: Code, db_session: DBSession) -> GetTutorialDistTypeSchema:
    return await get_distribution_type(code, db_session)


@dist_type_router.get("/getall")
@parameter_checker()
async def get_all_existing_distribution_types(db_session: DBSession) -> List[GetTutorialDistTypeSchema]:
    return await get_all_distribution_types(db_session)
