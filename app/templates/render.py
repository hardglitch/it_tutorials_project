from typing import Dict, List
from starlette.requests import Request
from app.common.constants import PageVars, templates
from app.db import DBSession
from app.language.crud import UILangCode, get_all_ui_langs
from app.language.schemas import LangAbbr, LanguageSchema
from app.user.auth import Token, decode_access_token, get_token
from app.user.schemas import TokenDataSchema


async def render_template(
        request: Request,
        db_session: DBSession | None = None,
        page_vars: Dict[str, ...] | None = None,
):
    context = {
        "request": request,
    }

    if page_vars: context.update(page_vars)

    if page_vars[PageVars.page] != PageVars.Page.exception:
        token: Token = get_token(request, safe_mode=True)
        auth: bool = False if token == "None" or not token else True

        if auth and not context.get("current_user"):
            current_user_data: TokenDataSchema = decode_access_token(token)
            context.update({"current_user": current_user_data})

        context.update({"auth": auth})

    try:
        ui_lang_code: UILangCode = page_vars[PageVars.ui_lang_code]
    except KeyError:
        ui_lang_code = None

    if db_session and ui_lang_code:
        ui_langs: List[LanguageSchema] = await get_all_ui_langs(db_session=db_session)
        ui_lang: LangAbbr = next(lang.abbreviation for lang in ui_langs if lang.lang_code == ui_lang_code)
        context.update({
            "ui_langs": ui_langs,
            "ui_lang": ui_lang.upper(),
        })

    return templates.TemplateResponse(
        name="base.html",
        context=context,
    )
