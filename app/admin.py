from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from app.common.constants import PageVars
from app.db import DBSession
from app.language.crud import UILangCode
from app.templates.render import render_template
from app.user.auth import is_admin


admin_router = APIRouter(prefix="", tags=["ADMIN"])


@admin_router.get("/admin")
async def admin_redirect(ui_lang_code: UILangCode) -> Response:
    response = RedirectResponse(url=f"/{ui_lang_code}/admin", status_code=status.HTTP_302_FOUND)
    return response


@admin_router.get("/{ui_lang_code}/admin")
async def admin(ui_lang_code: UILangCode, db_session: DBSession, request: Request) -> Response:
    if await is_admin(request=request, db_session=db_session, safe_mode=True):
        page_vars = {
            PageVars.page: PageVars.Page.admin,
            PageVars.ui_lang_code: ui_lang_code,
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
