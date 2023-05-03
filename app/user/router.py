from typing import Annotated, List
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from app.common.constants import AccessToken
from app.common.responses import ResponseSchema
from app.db import DBSession
from app.tools import parameter_checker
from app.user.crud import add_user, delete_user, edit_user, get_all_users, get_user
from app.user.exceptions import AuthenticateExceptions
from app.user.schemas import AddUserSchema, AuthUserSchema, EditUserSchema, GetUserSchema
from app.user.auth import UserID, authenticate_user, is_admin, create_access_token, decode_access_token, \
    get_token, is_me

user_router = APIRouter(prefix="/user", tags=["user"])
FormData = Annotated[OAuth2PasswordRequestForm, Depends()]


@user_router.post("/reg")
@parameter_checker()
async def user_registration(user: AddUserSchema, db_session: DBSession) -> GetUserSchema:
    return await add_user(user, db_session)


@user_router.post("/login")
@parameter_checker()
async def login(form_data: FormData, db_session: DBSession) -> Response:
    """This one creates an Access Token and redirects to the Current User profile"""
    user_data: AuthUserSchema = await authenticate_user(form_data.username, form_data.password, db_session)
    token: str = create_access_token(user_data)
    response = RedirectResponse(url="/user/me", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key=AccessToken.name, value=token, httponly=True, max_age=AccessToken.exp_delta)
    return response


@user_router.post("/logout")
@parameter_checker()
async def logout(request: Request) -> Response:
    if not get_token(request): raise AuthenticateExceptions.TOKEN_NOT_FOUND
    response = RedirectResponse(url="/", status_code=status.HTTP_200_OK)
    response.delete_cookie(key=AccessToken.name, httponly=True)
    return response


@user_router.put("/{user_id}/edit")
@parameter_checker()
async def edit_existing_user(request: Request, user_id: UserID, user_data: EditUserSchema, db_session: DBSession) -> ResponseSchema:
    if is_me(user_id, request) or await is_admin(request, db_session): return await edit_user(user_id, user_data, db_session)


@user_router.post("/{user_id}/del")
@parameter_checker()
async def delete_existing_user(request: Request, user_id: UserID, db_session: DBSession) -> ResponseSchema:
    if is_me(user_id, request) or await is_admin(request, db_session): return await delete_user(user_id, db_session)


@user_router.get("/me")
@parameter_checker()
async def get_current_user(request: Request, db_session: DBSession) -> GetUserSchema:
    user_id: int = decode_access_token(get_token(request)).id
    return await get_user(user_id, db_session)


@user_router.get("/get-all")
@parameter_checker()
async def get_all_existing_users(db_session: DBSession) -> List[GetUserSchema]:
    return await get_all_users(db_session)


@user_router.get("/{user_id}")
@parameter_checker()
async def get_existing_user(user_id: UserID, db_session: DBSession) -> GetUserSchema:
    return await get_user(user_id, db_session)
