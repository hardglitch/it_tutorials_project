from datetime import timedelta
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
from src.user.schemas import AddUserScheme, AuthUserScheme, EditUserScheme, GetUserScheme
from src.user.auth import Token, authenticate_user, create_access_token, decode_access_token, is_admin, \
    validate_access_token
from src.constants.exceptions import AuthenticateExceptions


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/reg")
async def user_registration(
        user: AddUserScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    return UserResponses.USER_CREATED\
        if await add_user(user, async_session)\
        else UserResponses.USER_NOT_CREATED


# This creates an Access Token and redirects to the Current User profile
@user_router.post("/login", response_class=HTMLResponse)
async def login(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        async_session: AsyncSession = Depends(get_session)
) -> RedirectResponse:

    user: AuthUserScheme = await authenticate_user(form_data.username, form_data.password, async_session)
    if not user: raise AuthenticateExceptions.INCORRECT_PARAMETERS

    token = create_access_token(
        user_name=user.name,
        user_id=user.id,
        exp_time=timedelta(minutes=AccessToken.expiration_time)
    )
    if not token: raise AuthenticateExceptions.FAILED_TO_CREATE_TOKEN

    # Redirect to the Current User profile
    response = RedirectResponse(url=f"/user/me", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key=AccessToken.name, value=token, httponly=True, max_age=AccessToken.expiration_time)

    return response


@user_router.post("/logout", response_class=HTMLResponse)
async def logout(request: Request, response: Response) -> None:
    token: Token = request.cookies.get(AccessToken.name)
    if token: return response.delete_cookie(key=AccessToken.name)


@user_router.put("/{user_id}/edit")
async def edit_existing_user(
        request: Request,
        user_id: Annotated[int, Path(title="User ID", ge=0)],
        new_user_data: EditUserScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    token: Token = request.cookies.get(AccessToken.name)
    if validate_access_token(user_id, token):
        return UserResponses.USER_UPDATED \
            if await edit_user(user_id, new_user_data, async_session) \
            else UserResponses.USER_NOT_UPDATED
    else:
        return UserResponses.ACCESS_DENIED


@user_router.post("/{user_id}/del")
async def delete_existing_user(
        request: Request,
        user_id: Annotated[int, Path(title="User ID", ge=0)],
        async_session: AsyncSession = Depends(get_session)
) -> str:

    token: Token = request.cookies.get(AccessToken.name)
    if validate_access_token(user_id, token) or await is_admin(token, async_session):
        return CommonResponses.SUCCESS if await delete_user(user_id, async_session) \
            else UserResponses.ACCESS_DENIED
    else:
        return UserResponses.ACCESS_DENIED


@user_router.get("/me")
async def get_current_user(
        request: Request,
        async_session: AsyncSession = Depends(get_session)
) -> GetUserScheme | str:

    token: Token | None = request.cookies.get(AccessToken.name)
    if not token: raise AuthenticateExceptions.TOKEN_NOT_FOUND

    user_id: int = int(decode_access_token(token)[AccessToken.user_id])

    decoded_user: GetUserScheme | None = await get_user(user_id, async_session)
    if not decoded_user: return UserResponses.USER_NOT_FOUND

    return decoded_user if decoded_user else UserResponses.USER_NOT_FOUND


@user_router.get("/{user_id}")
async def get_existing_user(
        user_id: Annotated[int, Path(title="User ID", ge=0)],
        async_session: AsyncSession = Depends(get_session)
) -> GetUserScheme | str:

    decoded_user: GetUserScheme | None = await get_user(user_id, async_session)
    if not decoded_user: return UserResponses.USER_NOT_FOUND
    return decoded_user if decoded_user else UserResponses.USER_NOT_FOUND
