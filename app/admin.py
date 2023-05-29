from typing import List
from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from app.common.constants import Credential, DecodedCredential, PageVars
from app.db import DBSession
from app.language.crud import UILangCode, get_all_langs
from app.language.schemas import LanguageSchema
from app.render import render_template
from app.tutorial.dist_type.crud import get_all_dist_types
from app.tutorial.dist_type.schemas import DistTypeSchema
from app.tutorial.theme.crud import get_all_themes
from app.tutorial.theme.schemas import ThemeSchema
from app.tutorial.type.crud import get_all_types
from app.tutorial.type.schemas import TypeSchema
from app.user.auth import is_admin
from app.user.crud import get_all_users
from app.user.schemas import UserSchema


admin_router = APIRouter(prefix="/adm", tags=["ADMIN"])


@admin_router.get("/")
async def admin_redirect(ui_lang_code: UILangCode) -> Response:
    response = RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_302_FOUND)
    return response


@admin_router.get("/{ui_lang_code}")
async def admin(ui_lang_code: UILangCode, db_session: DBSession, request: Request) -> Response:
    if await is_admin(request=request, db_session=db_session, safe_mode=True):
        tutor_types: List[TypeSchema] = await get_all_types(
            db_session=db_session,
        )
        tutor_themes: List[ThemeSchema] = await get_all_themes(
            db_session=db_session,
        )
        tutor_dist_types: List[DistTypeSchema] = await get_all_dist_types(
            db_session=db_session,
        )
        tutor_langs: List[LanguageSchema] = await get_all_langs(
            db_session=db_session,
        )
        users: List[UserSchema] = await get_all_users(
            db_session=db_session,
        )
        page_vars = {
            PageVars.page: PageVars.Page.admin,
            PageVars.ui_lang_code: ui_lang_code,
            "admin_js": True,
            "tutor_types": tutor_types,
            "tutor_themes": tutor_themes,
            "tutor_dist_types": tutor_dist_types,
            "tutor_langs": tutor_langs,
            "users": users,
            "credential": Credential,
            "decoded_credential": DecodedCredential,
        }
        return await render_template(
            request=request,
            db_session=db_session,
            page_vars=page_vars,
        )
    else:
        page_vars = {
            PageVars.page: "",
            PageVars.ui_lang_code: ui_lang_code,
            "is_adm": True,
        }
        return await render_template(
            request=request,
            db_session=db_session,
            page_vars=page_vars,
        )
