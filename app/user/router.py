from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response
from ..common.constants import AccessToken, PageVars
from ..db import DBSession
from ..language.crud import UILangCode
from ..templates.render import render_template
from ..tools import parameter_checker
from ..user.auth import Token, authenticate_user, create_access_token, is_me_or_admin, get_token
from ..user.crud import add_user, delete_user, edit_user, get_user
from ..user.schemas import EMail, Password, UserID, UserSchema, ValidUserName


user_router = APIRouter(prefix="", tags=["user"])


@user_router.get("/{ui_lang_code}/user/reg")
@parameter_checker()
async def reg_page(
        ui_lang_code: UILangCode,
        request: Request,
        db_session: DBSession,
) -> Response:

    page_vars = {
        PageVars.page: PageVars.Page.reg,
        PageVars.ui_lang_code: ui_lang_code,
    }
    return await render_template(
        request=request,
        db_session=db_session,
        ui_lang_code=ui_lang_code,
        page_vars=page_vars,
    )


@user_router.post("/{ui_lang_code}/user/add", response_model_exclude_none=True)
@parameter_checker()
async def add__user(
        name: Annotated[ValidUserName, Form()],
        email: Annotated[EMail, Form()],
        password: Annotated[Password, Form()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
) -> Response:

    if await add_user(
        UserSchema(
            name=name,
            email=email,
            password=password,
        ),
        db_session=db_session
    ):
        return RedirectResponse(url=f"/{ui_lang_code}", status_code=status.HTTP_201_CREATED)


@user_router.post("/{ui_lang_code}/user/login")
@parameter_checker()
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
) -> Response:

    """This one creates an Access Token and redirects to the Current User profile"""
    user_id, user_name = await authenticate_user(
        user_name=form_data.username, user_pwd=SecretStr(form_data.password), db_session=db_session
    )
    token: Token = create_access_token(uid=user_id, name=user_name)
    response = RedirectResponse(url=f"/{ui_lang_code}", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key=AccessToken.name, value=token, httponly=True, secure=True, max_age=AccessToken.exp_delta)
    return response


@user_router.get("/{ui_lang_code}/user/logout", dependencies=[Depends(get_token)])
@parameter_checker()
async def logout(ui_lang_code: UILangCode) -> Response:
    response = RedirectResponse(url=f"/{ui_lang_code}", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key=AccessToken.name, httponly=True, secure=True)
    return response


@user_router.post("/{ui_lang_code}/user/{user_id}/edit", dependencies=[Depends(is_me_or_admin)])
@parameter_checker()
async def edit__user(
        user_id: UserID,
        user_name: Annotated[ValidUserName, Form()],
        email: Annotated[EMail, Form()],
        password: Annotated[Password, Form()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
) -> Response:

    if await edit_user(
        UserSchema(
            id=user_id,
            name=user_name,
            email=email,
            password=password,
        ),
        db_session=db_session
    ):
        return RedirectResponse(url=f"/{ui_lang_code}/user/{user_id}", status_code=status.HTTP_303_SEE_OTHER)


@user_router.post("/{ui_lang_code}/user/{user_id}/del", dependencies=[Depends(is_me_or_admin)])
@parameter_checker()
async def delete__user(
        user_id: UserID,
        ui_lang_code: UILangCode,
        db_session: DBSession
) -> Response:

    if await delete_user(user_id=user_id, db_session=db_session):
        return RedirectResponse(url=f"/{ui_lang_code}", status_code=status.HTTP_302_FOUND)


@user_router.get("/{ui_lang_code}/user/{user_id}/me", response_class=HTMLResponse, dependencies=[Depends(is_me_or_admin)])
@parameter_checker()
async def get__me(
        user_id: UserID,
        ui_lang_code: UILangCode,
        request: Request,
        db_session: DBSession
) -> Response:

    current_user_data: UserSchema = await get_user(user_id=user_id, db_session=db_session, is_me=True)

    page_vars = {
        PageVars.page: PageVars.Page.profile_ext,
        PageVars.ui_lang_code: ui_lang_code,
        PageVars.current_user: current_user_data,
    }
    return await render_template(
        request=request,
        db_session=db_session,
        ui_lang_code=ui_lang_code,
        page_vars=page_vars,
    )


@user_router.get("/{ui_lang_code}/user/{user_id}", response_class=HTMLResponse)
@parameter_checker()
async def get__user(
        user_id: UserID,
        ui_lang_code: UILangCode,
        request: Request,
        db_session: DBSession
) -> Response:

    userdata: UserSchema = await get_user(user_id=user_id, db_session=db_session)

    page_vars = {
        PageVars.page: PageVars.Page.profile,
        PageVars.ui_lang_code: ui_lang_code,
        "userdata": userdata
    }
    return await render_template(
        request=request,
        db_session=db_session,
        ui_lang_code=ui_lang_code,
        page_vars=page_vars,
    )

# @user_router.get("/{ui_lang_code}/user/", response_model_exclude_none=True)
# @parameter_checker()
# async def get__all_users(ui_lang_code: UILangCode, db_session: DBSession) -> List[UserSchema]:
#     users = await get_all_users(db_session=db_session)
#
#     return templates.TemplateResponse(
#         name="profile.html",
#         context={
#             "request": request,
#             "ui_lang_code": ui_lang_code,
#             "auth": auth,
#             "current_user": current_user_data,
#             "userdata": userdata
#         }
#     )
#
