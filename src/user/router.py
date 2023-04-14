from datetime import timedelta
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, Path, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse
from src.db import get_session
from src.db_const import Credential
from src.responses import UserResponses
from src.user.schemas import DecryptedUserReadScheme, UserCreateScheme
from src.user.auth import authenticate_user, create_access_token, create_user, safe_get_user
from src.exceptions import AuthenticateExceptions


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/registration")
async def user_registration(user: UserCreateScheme, async_session: AsyncSession = Depends(get_session)) -> Dict[str, str]:
    return await create_user(user=user, async_session=async_session)


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
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)    # TODO: Redirect to the Current User profile
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=60)

    return response


@user_router.post("/{user_id}")
async def safe_read_user(
        user_id: Annotated[int, Path(title="User ID")],
        async_session: AsyncSession = Depends(get_session)
):
    user = await safe_get_user(user_id, async_session)
    decrypted_user = DecryptedUserReadScheme(
        name=user.name,
        credential=Credential(user.credential).name,
        is_active=user.is_active,
        rating=user.rating,
    )
    return decrypted_user if user else UserResponses.USER_NOT_FOUND
