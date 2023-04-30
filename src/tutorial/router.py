from fastapi import APIRouter
from starlette.requests import Request
from src.constants.exceptions import UserExceptions
from src.constants.responses import ResponseScheme
from src.db import DBSession
from src.tools import parameter_checker
from src.tutorial.crud import TutorID, add_tutorial, delete_tutorial, edit_tutorial, get_decoded_tutorial, get_tutorial
from src.tutorial.dist_type.router import dist_type_router
from src.tutorial.schemas import AddTutorialScheme, EditTutorialScheme, GetTutorialScheme
from src.tutorial.theme.router import theme_router
from src.tutorial.type.router import type_router
from src.user.auth import decode_access_token, get_token_from_cookie, is_admin


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
@parameter_checker()
async def get_existing_tutorial(tutor_id: TutorID, db_session: DBSession) -> AddTutorialScheme:
    return await get_tutorial(tutor_id, db_session)


# for tests
@tutorial_router.get("/getdecoded/{tutor_id}")
@parameter_checker()
async def get_existing_decoded_tutorial(tutor_id: TutorID, db_session: DBSession) -> GetTutorialScheme:
    return await get_decoded_tutorial(tutor_id, db_session)
