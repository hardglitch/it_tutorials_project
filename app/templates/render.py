import json
from typing import Dict, List
from starlette.requests import Request
from app.common.constants import Credential, DEFAULT_UI_LANGUAGE, PageVars, templates, templates_dir
from app.common.exceptions import LocaleExceptions
from app.db import DBSession
from app.language.crud import UILangCode, get_all_ui_langs
from app.language.schemas import LangAbbr, LanguageSchema
from app.user.auth import Token, decode_access_token, get_token, is_admin, is_this
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
        if token and (is_adm := await is_this(
                credential=Credential.admin, token=token, db_session=db_session, safe_mode=True)):
            context.update({"is_adm": is_adm})

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
        context.update(get_locale(ui_lang))

    return templates.TemplateResponse(
        name="base.html",
        context=context,
    )


def get_locale(ui_lang_abbr: LangAbbr = DEFAULT_UI_LANGUAGE.lower()) -> Dict[str, str]:
    try:
        a = templates_dir.joinpath("locales").joinpath(ui_lang_abbr)
        with open(templates_dir.joinpath("locales").joinpath(ui_lang_abbr), encoding="utf-8") as file:
            data = json.load(file)
            if all(
                    (
                        isinstance(item[0], str) and len(item[0]) < 256 and item[0].startswith("loc_") and
                        isinstance(item[1], str) and len(item[1]) < 256
                    )
                    for item in data.items()
            ):
                return data
            raise LocaleExceptions.WRONG_LOCALE

    except (FileNotFoundError, FileExistsError):
        if ui_lang_abbr != DEFAULT_UI_LANGUAGE.lower():
            get_locale()
        else:
            raise LocaleExceptions.LOCALE_NOT_FOUND
