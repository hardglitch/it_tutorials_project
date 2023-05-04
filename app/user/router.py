from typing import Annotated, List
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from app.common.constants import AccessToken
from app.common.responses import ResponseSchema
from app.db import DBSession
from app.tools import parameter_checker
from app.user.auth import authenticate_user, decode_access_token, get_token, is_admin, is_me
from app.user.crud import add_user, delete_user, edit_user, get_all_users, get_user
from app.user.exceptions import AuthenticateExceptions, UserExceptions
from app.user.schemas import EMail, Password, UserID, UserName, UserSchema


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/reg", response_model_exclude_none=True)
@parameter_checker()
async def user_registration(
        user_name: Annotated[UserName, Form()],
        email: Annotated[EMail, Form()],
        password: Annotated[Password, Form()],
        db_session: DBSession
) -> UserSchema:

    user = UserSchema(
        name=user_name,
        email=email,
        password=password,
    )
    return await add_user(user, db_session)


@user_router.post("/login", response_model_exclude_none=True)
@parameter_checker()
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db_session: DBSession
) -> Response:

    """This one creates an Access Token and redirects to the Current User profile"""
    token = await authenticate_user(user_name=form_data.username, user_pwd=SecretStr(form_data.password), db_session=db_session)
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


@user_router.post("/{user_id}/edit", response_model_exclude_none=True)
@parameter_checker()
async def edit_existing_user(
        request: Request,
        user_id: UserID,
        user_name: Annotated[UserName, Form()],
        email: Annotated[EMail, Form()],
        password: Annotated[Password, Form()],
        db_session: DBSession
) -> ResponseSchema:

    if not is_me(user_id, request) and not await is_admin(request, db_session):
        raise UserExceptions.ACCESS_DENIED

    user = UserSchema(
        id=user_id,
        name=user_name,
        email=email,
        password=password,
    )
    return await edit_user(user, db_session)


@user_router.post("/{user_id}/del", response_model_exclude_none=True)
@parameter_checker()
async def delete_existing_user(
        request: Request,
        user_id: UserID,
        db_session: DBSession
) -> ResponseSchema:

    if not is_me(user_id, request) and not await is_admin(request, db_session):
        raise UserExceptions.ACCESS_DENIED
    return await delete_user(user_id, db_session)


@user_router.get("/me", response_model_exclude_none=True)
@parameter_checker()
async def get_current_user(request: Request, db_session: DBSession) -> UserSchema:
    return await get_user(decode_access_token(get_token(request)).id, db_session)


@user_router.get("/get-all", response_model_exclude_none=True)
@parameter_checker()
async def get_all_existing_users(db_session: DBSession) -> List[UserSchema]:
    return await get_all_users(db_session)


@user_router.get("/{user_id}", response_model_exclude_none=True)
@parameter_checker()
async def get_existing_user(user_id: UserID, db_session: DBSession) -> UserSchema:
    return await get_user(user_id, db_session)
