from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response
from ..common.constants import AccessToken, Credential, PageVars
from ..db import DBSession
from ..language.crud import UILangCode
from app.render import render_template
from ..tools import parameter_checker
from ..user.auth import Token, authenticate_user, create_access_token, is_admin, is_me_or_admin, get_token
from ..user.crud import add_user, delete_user, edit_user, get_user, update_user_status
from ..user.schemas import EMail, IsActive, Password, UserID, UserSchema, ValidUserName


user_router = APIRouter(prefix="/usr", tags=["User"])


@user_router.get("/{ui_lang_code}/reg", response_class=HTMLResponse)
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
        page_vars=page_vars,
    )


@user_router.post("/{ui_lang_code}/add", response_model_exclude_none=True)
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
        return RedirectResponse(url=f"/tt/{ui_lang_code}", status_code=status.HTTP_201_CREATED)


@user_router.post("/{ui_lang_code}/login")
@parameter_checker()
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
        is_adm: bool | None = None,
) -> Response:

    """This one creates an Access Token and redirects to the Current User profile"""
    user_id, user_name = await authenticate_user(
        user_name=form_data.username,
        user_pwd=SecretStr(form_data.password),
        db_session=db_session,
        is_adm=is_adm,
    )
    token: Token = create_access_token(uid=user_id, name=user_name)
    adm_str = "/adm" if is_adm else "/tt"
    response = RedirectResponse(url=f"{adm_str}/{ui_lang_code}", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key=AccessToken.name, value=token, httponly=True, secure=True, max_age=AccessToken.exp_delta)
    return response


@user_router.get("/{ui_lang_code}/logout", dependencies=[Depends(get_token)])
@parameter_checker()
async def logout(ui_lang_code: UILangCode) -> Response:
    response = RedirectResponse(url=f"/tt/{ui_lang_code}", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key=AccessToken.name, httponly=True, secure=True)
    return response


@user_router.post("/{ui_lang_code}/{user_id}/edit", dependencies=[Depends(is_me_or_admin)])
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
        return RedirectResponse(url=f"/usr/{ui_lang_code}/{user_id}", status_code=status.HTTP_303_SEE_OTHER)


@user_router.post("/{ui_lang_code}/{user_id}/upd", dependencies=[Depends(is_admin)])
@parameter_checker()
async def update__user_status(
        user_id: UserID,
        is_active: Annotated[IsActive, Form()],
        credential: Annotated[Credential, Form()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
) -> Response:

    if await update_user_status(
        user_id=user_id,
        is_active=is_active,
        credential=credential,
        db_session=db_session
    ):
        return RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_302_FOUND)


@user_router.post("/{ui_lang_code}/{user_id}/del", dependencies=[Depends(is_me_or_admin)])
@parameter_checker()
async def delete__user(
        user_id: UserID,
        ui_lang_code: UILangCode,
        db_session: DBSession
) -> Response:

    if await delete_user(user_id=user_id, db_session=db_session):
        response = RedirectResponse(url=f"/tt/{ui_lang_code}", status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key=AccessToken.name, secure=True, httponly=True)
        return response


@user_router.get("/{ui_lang_code}/{user_id}/me", response_class=HTMLResponse, dependencies=[Depends(is_me_or_admin)])
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
        page_vars=page_vars,
    )


@user_router.get("/{ui_lang_code}/{user_id}", response_class=HTMLResponse)
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
        page_vars=page_vars,
    )
