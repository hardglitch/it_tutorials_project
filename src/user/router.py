from typing import Annotated
from fastapi import APIRouter, Depends, Path, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from src.db import get_session
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, UserResponses
from src.user.crud import add_user, delete_user, edit_user, get_user
from src.user.schemas import AccessTokenScheme, AddUserScheme, AuthUserScheme, EditUserScheme, GetUserScheme
from src.user.auth import Token, authenticate_user, create_access_token, decode_access_token, is_admin, \
    validate_access_token
from src.constants.exceptions import AuthenticateExceptions


# Aliases
DBSession = Annotated[AsyncSession, Depends(get_session)]
UserID = Annotated[int, Path(title="User ID", ge=0)]

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/reg")
async def user_registration(user: AddUserScheme, db_session: DBSession) -> str:
    return UserResponses.USER_CREATED\
        if await add_user(user, db_session)\
        else UserResponses.USER_NOT_CREATED


# This creates an Access Token and redirects to the Current User profile
@user_router.post("/login", response_class=HTMLResponse)
async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db_session: DBSession
) -> RedirectResponse:

    user: AuthUserScheme = await authenticate_user(form_data.username, form_data.password, db_session)
    if not user: raise AuthenticateExceptions.INCORRECT_PARAMETERS

    token: str = create_access_token(AccessTokenScheme(name=user.name, id=user.id))
    if not token: raise AuthenticateExceptions.FAILED_TO_CREATE_TOKEN

    # Redirect to the Current User profile
    response = RedirectResponse(url=f"/user/me", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key=AccessToken.name, value=token, httponly=True, max_age=AccessToken.exp_delta)

    return response


@user_router.post("/logout", response_class=HTMLResponse)
async def logout(request: Request, response: Response) -> None:
    token: Token = request.cookies.get(AccessToken.name)
    if token: return response.delete_cookie(key=AccessToken.name, httponly=True)


@user_router.put("/{user_id}/edit")
async def edit_existing_user(
        request: Request,
        user_id: UserID,
        new_user_data: EditUserScheme,
        db_session: DBSession
) -> str:

    token: Token = request.cookies.get(AccessToken.name)
    if validate_access_token(user_id, token):
        return UserResponses.USER_UPDATED \
            if await edit_user(user_id, new_user_data, db_session) \
            else UserResponses.USER_NOT_UPDATED
    else:
        return UserResponses.ACCESS_DENIED


@user_router.post("/{user_id}/del")
async def delete_existing_user(request: Request, user_id: UserID, db_session: DBSession) -> str:
    token: Token = request.cookies.get(AccessToken.name)
    if validate_access_token(user_id, token) or await is_admin(token, db_session):
        return CommonResponses.SUCCESS if await delete_user(user_id, db_session) \
            else UserResponses.ACCESS_DENIED
    else:
        return UserResponses.ACCESS_DENIED


@user_router.get("/me")
async def get_current_user(request: Request, db_session: DBSession) -> GetUserScheme | str:
    token: Token | None = request.cookies.get(AccessToken.name)
    if not token: raise AuthenticateExceptions.TOKEN_NOT_FOUND

    user_id: int = decode_access_token(token).id

    decoded_user: GetUserScheme | None = await get_user(user_id, db_session)
    if not decoded_user: return UserResponses.USER_NOT_FOUND
    return decoded_user if decoded_user else UserResponses.USER_NOT_FOUND


@user_router.get("/{user_id}")
async def get_existing_user(user_id: UserID, db_session: DBSession) -> GetUserScheme | str:
    decoded_user: GetUserScheme | None = await get_user(user_id, db_session)
    if not decoded_user: return UserResponses.USER_NOT_FOUND
    return decoded_user if decoded_user else UserResponses.USER_NOT_FOUND
