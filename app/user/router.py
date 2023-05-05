from typing import Annotated, List
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from starlette import status
from starlette.responses import RedirectResponse, Response
from app.common.constants import AccessToken
from app.common.responses import ResponseSchema
from app.tools import parameter_checker
from app.user.auth import Token, authenticate_user, create_access_token, is_me_or_admin, get_token
from app.user.crud import add_user, delete_user, edit_user, get_all_users, get_user
from app.user.schemas import EMail, Password, UserID, UserName, UserSchema


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/reg", response_model_exclude_none=True)
@parameter_checker()
async def add__user(
        user_name: Annotated[UserName, Form()],
        email: Annotated[EMail, Form()],
        password: Annotated[Password, Form()],
) -> UserSchema:

    return await add_user(
        UserSchema(
            name=user_name,
            email=email,
            password=password,
        )
    )


@user_router.post("/login", response_model_exclude_none=True)
@parameter_checker()
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Response:
    """This one creates an Access Token and redirects to the Current User profile"""
    user_id, user_name = await authenticate_user(form_data.username, SecretStr(form_data.password))
    token: Token = create_access_token(uid=user_id, name=user_name)
    response = RedirectResponse(url=f"/user/{user_id}", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key=AccessToken.name, value=token, httponly=True, max_age=AccessToken.exp_delta)
    return response


@user_router.post("/logout", dependencies=[Depends(get_token)])
@parameter_checker()
async def logout() -> Response:
    response = RedirectResponse(url="/", status_code=status.HTTP_200_OK)
    response.delete_cookie(key=AccessToken.name, httponly=True)
    return response


@user_router.post("/{user_id}/edit", response_model_exclude_none=True, dependencies=[Depends(is_me_or_admin)])
@parameter_checker()
async def edit__user(
        user_id: UserID,
        user_name: Annotated[UserName, Form()],
        email: Annotated[EMail, Form()],
        password: Annotated[Password, Form()],
) -> ResponseSchema:

    return await edit_user(
        UserSchema(
            id=user_id,
            name=user_name,
            email=email,
            password=password,
        )
    )


@user_router.post("/{user_id}/del", response_model_exclude_none=True, dependencies=[Depends(is_me_or_admin)])
@parameter_checker()
async def delete__user(user_id: UserID) -> ResponseSchema:
    return await delete_user(user_id)


@user_router.get("/get-all", response_model_exclude_none=True)
@parameter_checker()
async def get__all_users() -> List[UserSchema]:
    return await get_all_users()


@user_router.get("/{user_id}", response_model_exclude_none=True)
@parameter_checker()
async def get__user(user_id: UserID) -> UserSchema:
    return await get_user(user_id)
