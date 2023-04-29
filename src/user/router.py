from typing import Annotated
from fastapi import APIRouter, Depends, Path, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from src.constants.constants import AccessToken
from src.constants.responses import ResponseScheme, UserResponses
from src.db import DBSession
from src.user.crud import add_user, delete_user, edit_user, get_user
from src.user.schemas import AccessTokenScheme, AddUserScheme, AuthUserScheme, EditUserScheme, GetUserScheme
from src.user.auth import authenticate_user, check_credential, create_access_token, decode_access_token, \
    get_token_from_cookie
from src.constants.exceptions import CommonExceptions


user_router = APIRouter(prefix="/user", tags=["user"])
UserID = Annotated[int, Path(title="User ID", ge=0)]
FormData = Annotated[OAuth2PasswordRequestForm, Depends()]


@user_router.post("/reg")
async def user_registration(user: AddUserScheme, db_session: DBSession) -> GetUserScheme:
    try:
        return await add_user(user, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


# This creates an Access Token and redirects to the Current User profile
@user_router.post("/login")
async def login(form_data: FormData, db_session: DBSession) -> Response:
    try:
        user: AuthUserScheme = await authenticate_user(form_data.username, form_data.password, db_session)
        token: str = create_access_token(AccessTokenScheme(name=user.name, id=user.id))

        # Redirect to the Current User profile
        response = RedirectResponse(url="/user/me", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key=AccessToken.name, value=token, httponly=True, max_age=AccessToken.exp_delta)
        return response

    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@user_router.post("/logout")
async def logout(request: Request) -> Response:
    try:
        if get_token_from_cookie(request):
            response = RedirectResponse(url="/", status_code=status.HTTP_200_OK)
            response.delete_cookie(key=AccessToken.name, httponly=True)
            return response
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@user_router.put("/{user_id}/edit")
async def edit_existing_user(request: Request, user_id: UserID, new_user_data: EditUserScheme, db_session: DBSession) -> ResponseScheme:
    try:
        if not check_credential(user_id, get_token_from_cookie(request), db_session): raise UserResponses.ACCESS_DENIED
        return await edit_user(user_id, new_user_data, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@user_router.post("/{user_id}/del")
async def delete_existing_user(request: Request, user_id: UserID, db_session: DBSession) -> ResponseScheme:
    try:
        if not check_credential(user_id, get_token_from_cookie(request), db_session): raise UserResponses.ACCESS_DENIED
        return await delete_user(user_id, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@user_router.get("/me")
async def get_current_user(request: Request, db_session: DBSession) -> GetUserScheme:
    try:
        user_id: int = decode_access_token(get_token_from_cookie(request)).id
        return await get_user(user_id, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS


@user_router.get("/{user_id}")
async def get_existing_user(user_id: UserID, db_session: DBSession) -> GetUserScheme:
    try:
        return await get_user(user_id, db_session)
    except (TypeError, ValueError):
        raise CommonExceptions.INVALID_PARAMETERS
