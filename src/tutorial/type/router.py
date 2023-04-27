from typing import Annotated, List
from fastapi import APIRouter, Path
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, UserResponses
from src.db import DBSession
from src.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from src.tutorial.type.crud import add_tutorial_type, delete_tutorial_type, edit_tutorial_type, get_all_tutorial_types, \
    get_tutorial_type
from src.tutorial.type.schemas import GetTutorialTypeScheme
from src.user.auth import Token, is_admin


Code = Annotated[int, Path(title="A code of the Tutorial Type", ge=0)]

type_router = APIRouter(prefix="/type", tags=["tutorial type"])


@type_router.post("/add")
async def add_new_tutorial_type(
        request: Request,
        dist_type: AddWordToDictionaryScheme,
        db_session: DBSession
) -> str:

    if not all([request, dist_type, db_session]): return CommonResponses.FAILED

    token: Token = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await add_tutorial_type(dist_type, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@type_router.put("/edit")
async def edit_existing_tutorial_type(
        request: Request,
        dist_type: EditDictionaryScheme,
        db_session: DBSession
) -> str:

    if not all([request, dist_type, db_session]): return CommonResponses.FAILED

    token: Token = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await edit_tutorial_type(dist_type, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@type_router.post("/del/{code}")
async def delete_existing_tutorial_type(request: Request, code: Code, db_session: DBSession) -> str:
    if not all([request, code, db_session]): return CommonResponses.FAILED

    token: Token = request.cookies.get(AccessToken.name)
    if await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await delete_tutorial_type(code, db_session) \
            else CommonResponses.FAILED
    else:
        return UserResponses.ACCESS_DENIED


@type_router.get("/get/{code}")
async def get_existing_tutorial_type(code: Code, db_session: DBSession) -> GetTutorialTypeScheme | str:
    if not code or not db_session: return CommonResponses.FAILED
    tutor: GetTutorialTypeScheme | None = await get_tutorial_type(code, db_session)
    return tutor if tutor else CommonResponses.FAILED


@type_router.get("/getall")
async def get_all_existing_tutorial_types(db_session: DBSession) -> List[GetTutorialTypeScheme] | str:
    if not db_session: return CommonResponses.FAILED
    tutors: List[GetTutorialTypeScheme] | None = await get_all_tutorial_types(db_session)
    return tutors if tutors else CommonResponses.FAILED
