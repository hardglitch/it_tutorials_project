from typing import Annotated, List
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from ..common.constants import AccessToken, templates
from ..common.responses import ResponseSchema
from ..db import DBSession
from ..tools import parameter_checker
from ..user.auth import Token, authenticate_user, create_access_token, is_me_or_admin, get_token
from ..user.crud import add_user, delete_user, edit_user, get_all_users, get_user
from ..user.schemas import EMail, Password, UserID, UserSchema, ValidUserName


user_router = APIRouter(prefix="/user", tags=["user"], responses={401: {"detail": "Not auth"}})


@user_router.get("/reg")
async def reg_page(request: Request):
    return templates.TemplateResponse(
        name="reg.html",
        context={"request": request}
    )


@user_router.post("/add", response_model_exclude_none=True)
@parameter_checker()
async def add__user(
        name: Annotated[ValidUserName, Form()],
        email: Annotated[EMail, Form()],
        password: Annotated[Password, Form()],
        db_session: DBSession,
) -> Response:

    new_user_data = await add_user(
        UserSchema(
            name=name,
            email=email,
            password=password,
        ),
        db_session=db_session
    )
    response = RedirectResponse(url="/", status_code=status.HTTP_201_CREATED)
    return response


@user_router.post("/login")
@parameter_checker()
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db_session: DBSession,
) -> Response:

    """This one creates an Access Token and redirects to the Current User profile"""
    user_id, user_name = await authenticate_user(
        user_name=form_data.username, user_pwd=SecretStr(form_data.password), db_session=db_session
    )
    token: Token = create_access_token(uid=user_id, name=user_name)
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key=AccessToken.name, value=token, httponly=True, secure=True, max_age=AccessToken.exp_delta)
    return response


@user_router.get("/logout", dependencies=[Depends(get_token)])
@parameter_checker()
async def logout() -> Response:
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key=AccessToken.name, httponly=True, secure=True)
    return response


@user_router.put("/{user_id}/edit", dependencies=[Depends(is_me_or_admin)])
@parameter_checker()
async def edit__user(
        user_id: UserID,
        user_name: Annotated[ValidUserName, Form()],
        email: Annotated[EMail, Form()],
        password: Annotated[Password, Form()],
        db_session: DBSession,
) -> ResponseSchema:

    return await edit_user(
        UserSchema(
            id=user_id,
            name=user_name,
            email=email,
            password=password,
        ),
        db_session=db_session
    )


@user_router.post("/{user_id}/del", dependencies=[Depends(is_me_or_admin)])
@parameter_checker()
async def delete__user(user_id: UserID, db_session: DBSession) -> ResponseSchema:
    return await delete_user(user_id=user_id, db_session=db_session)


@user_router.get("/get-all", response_model_exclude_none=True)
@parameter_checker()
async def get__all_users(db_session: DBSession) -> List[UserSchema]:
    return await get_all_users(db_session=db_session)


@user_router.get("/{user_id}", response_model_exclude_none=True)
@parameter_checker()
async def get__user(user_id: UserID, db_session: DBSession) -> UserSchema:
    return await get_user(user_id=user_id, db_session=db_session)
