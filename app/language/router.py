from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, Path
from starlette import status
from starlette.responses import RedirectResponse, Response

from ..common.responses import ResponseSchema
from ..db import DBSession
from ..language.crud import LangCode, UILangCode, add_lang, delete_lang, edit_lang, get_all_langs, get_lang
from ..language.schemas import IsUILang, LanguageSchema, ValidLangAbbr, ValidLangValue
from ..tools import parameter_checker
from ..user.auth import is_admin


language_router = APIRouter(prefix="/lng", tags=["Language"])


@language_router.post("/{ui_lang_code}/add", dependencies=[Depends(is_admin)])
@parameter_checker()
async def add_language(
        lang_value: Annotated[ValidLangValue, Form(description="Any unicode value")],
        lang_abbr: Annotated[ValidLangAbbr, Form(description="3 chars, only english")],
        is_ui_lang: Annotated[IsUILang, Form()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
) -> Response:
    if await add_lang(
        LanguageSchema(
            lang_value=lang_value,
            abbreviation=lang_abbr,
            is_ui_lang=is_ui_lang,
        ),
        db_session=db_session
    ):
        return RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_200_OK)


@language_router.post("/{ui_lang_code}/{lang_code}/edit", dependencies=[Depends(is_admin)])
@parameter_checker()
async def edit_language(
        lang_code: Annotated[LangCode, Path()],
        lang_value: Annotated[ValidLangValue, Form()],
        lang_abbr: Annotated[ValidLangAbbr, Form()],
        is_ui_lang: Annotated[IsUILang, Form()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
) -> Response:

    if await edit_lang(
        LanguageSchema(
            lang_code=lang_code,
            lang_value=lang_value,
            abbreviation=lang_abbr,
            is_ui_lang=is_ui_lang,
        ),
        db_session=db_session
    ):
        return RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_302_FOUND)


@language_router.post("/{ui_lang_code}/{lang_code}/del", dependencies=[Depends(is_admin)])
@parameter_checker()
async def delete_language(
        lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
        ui_lang_code: UILangCode,
) -> Response:

    if await delete_lang(lang_code, db_session):
        return RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_200_OK)


@language_router.get("/{ui_lang_code}/{lang_code}", response_model_exclude_none=True)
@parameter_checker()
async def get_language(lang_code: Annotated[LangCode, Path()], db_session: DBSession) -> LanguageSchema:
    return await get_lang(lang_code, db_session)


@language_router.get("/{ui_lang_code}", response_model_exclude_none=True)
@parameter_checker()
async def get_all_languages(db_session: DBSession) -> List[LanguageSchema]:
    return await get_all_langs(db_session)
