from fastapi import APIRouter
from fastapi_cache.decorator import cache
from starlette.requests import Request
from app.constants.exceptions import UserExceptions
from app.constants.responses import ResponseScheme
from app.db import DBSession
from app.tools import parameter_checker
from app.tutorial.crud import TutorID, add_tutorial, delete_tutorial, edit_tutorial, get_decoded_tutorial, get_tutorial
from app.tutorial.dist_type.router import dist_type_router
from app.tutorial.schemas import AddTutorialScheme, EditTutorialScheme, GetDecodedTutorialScheme
from app.tutorial.theme.router import theme_router
from app.tutorial.type.router import type_router
from app.user.auth import decode_access_token, get_token_from_cookie, is_admin


tutorial_router = APIRouter(prefix="/tutorial", tags=["tutorial"])
tutorial_router.include_router(dist_type_router)
tutorial_router.include_router(theme_router)
tutorial_router.include_router(type_router)


@tutorial_router.post("/add")
@parameter_checker()
async def add_new_tutorial(request: Request, tutor: AddTutorialScheme, db_session: DBSession) -> ResponseScheme:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    tutor.who_added = decode_access_token(get_token_from_cookie(request)).id
    return await add_tutorial(tutor, db_session)


@tutorial_router.put("/edit/{tutor_id}")
@parameter_checker()
async def edit_existing_tutorial(request: Request, tutor_id: TutorID, tutor_data: EditTutorialScheme, db_session: DBSession) -> ResponseScheme:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await edit_tutorial(tutor_id, tutor_data, db_session)


@tutorial_router.post("/del/{tutor_id}")
@parameter_checker()
async def delete_existing_tutorial(request: Request, tutor_id: TutorID, db_session: DBSession) -> ResponseScheme:
    if not await is_admin(get_token_from_cookie(request), db_session): raise UserExceptions.ACCESS_DENIED
    return await delete_tutorial(tutor_id, db_session)


@tutorial_router.get("/get/{tutor_id}")
@cache(expire=60)
@parameter_checker()
async def get_existing_tutorial(tutor_id: TutorID, db_session: DBSession) -> AddTutorialScheme:
    return await get_tutorial(tutor_id, db_session)


# for test
@tutorial_router.get("/getdecoded/{tutor_id}")
@cache(expire=60)
@parameter_checker()
async def get_existing_decoded_tutorial(tutor_id: TutorID, db_session: DBSession) -> GetDecodedTutorialScheme:
    return await get_decoded_tutorial(tutor_id, db_session)
