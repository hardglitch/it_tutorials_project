from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from src.db import get_session
from src.constants.constants import AccessToken, Credential
from src.constants.responses import UserResponses
from src.user.schemas import DecryptedUserReadScheme, UserCreateScheme, UserUpdateScheme
from src.user.auth import authenticate_user, create_access_token, create_user, oauth2_scheme, safe_get_user,\
    update_user, validate_access
from src.constants.exceptions import AuthenticateExceptions


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/registration")
async def user_registration(
        user: UserCreateScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    return UserResponses.USER_CREATED\
        if await create_user(user, async_session)\
        else UserResponses.USER_ALREADY_EXISTS


# This creates an Access Token and redirects to the Current User profile
@user_router.post("/login", response_class=HTMLResponse)
async def login_for_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        async_session: AsyncSession = Depends(get_session)
) -> RedirectResponse:

    user = await authenticate_user(form_data.username, form_data.password, async_session)
    if not user: raise AuthenticateExceptions.TOKEN_EXCEPTION

    token = create_access_token(user_name=user.name, user_id=user.id, expires_delta=timedelta(minutes=20))
    if not token: raise AuthenticateExceptions.FAILED_TO_CREATE_TOKEN_EXCEPTION

    # Redirect to the Current User profile
    response = RedirectResponse(url=f"/user/{user.id}", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key=AccessToken.name, value=token, httponly=True, max_age=60)

    return response


@user_router.post("/logout", response_class=HTMLResponse)
async def logout(request: Request, response: Response) -> None:
    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if token: return response.delete_cookie(key=AccessToken.name)


@user_router.get("/{user_id}")
async def safe_read_user(
        user_id: Annotated[int, Path(title="User ID")],
        async_session: AsyncSession = Depends(get_session)
) -> DecryptedUserReadScheme | str:

    user = await safe_get_user(user_id, async_session)
    decrypted_user = DecryptedUserReadScheme(
        name=user.name,
        credential=Credential(user.credential).name,
        is_active=user.is_active,
        rating=user.rating,
    )
    return decrypted_user if user else UserResponses.USER_NOT_FOUND


@user_router.patch("/{user_id}")
async def secure_update_user(
        request: Request,
        user_id: Annotated[int, Path(title="User ID")],
        new_user_data: UserUpdateScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:
    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if validate_access(user_id, token):
        return UserResponses.USER_UPDATED \
            if await update_user(user_id, new_user_data, async_session) \
            else UserResponses.USER_NOT_UPDATED
    else:
        return UserResponses.ACCESS_DENIED
