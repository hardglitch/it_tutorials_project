from typing import Annotated, List
from fastapi import Depends
from fastapi_cache.decorator import cache
from sqlalchemy import ScalarResult, delete, select, update
from starlette.requests import Request

from ..common.constants import DEFAULT_UI_LANGUAGE
from ..common.exceptions import CommonExceptions
from ..common.responses import CommonResponses, ResponseSchema
from ..db import DBSession
from ..language.models import LanguageModel
from ..language.schemas import LangCode, LanguageSchema
from ..tools import db_checker


@db_checker()
async def add_lang(lang: LanguageSchema, db_session: DBSession) -> ResponseSchema:
    new_lang = LanguageModel(
        abbreviation=lang.abbreviation,
        value=lang.lang_value,
        is_ui_lang=lang.is_ui_lang
    )
    db_session.add(new_lang)
    await db_session.commit()
    return CommonResponses.CREATED


@db_checker()
async def edit_lang(lang: LanguageSchema, db_session: DBSession) -> ResponseSchema:
    await db_session.execute(
        update(LanguageModel)
        .where(LanguageModel.code == lang.lang_code)
        .values(
            abbreviation=lang.abbreviation,
            value=lang.lang_value,
            is_ui_lang=lang.is_ui_lang
        )
    )
    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def delete_lang(lang_code: LangCode, db_session: DBSession) -> ResponseSchema:
    await db_session.execute(
        delete(LanguageModel)
        .where(LanguageModel.code == lang_code)
    )
    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def get_lang(lang_code: LangCode, db_session: DBSession) -> LanguageSchema:
    lang_from_db: LanguageModel | None = await db_session.get(LanguageModel, lang_code)
    if not lang_from_db: raise CommonExceptions.NOTHING_FOUND
    return LanguageSchema(
        abbreviation=lang_from_db.abbreviation,
        lang_value=lang_from_db.value,
        is_ui_lang=lang_from_db.is_ui_lang
    )


@db_checker()
async def ui_lang(db_session: DBSession, ui_lang_code: LangCode | None = None) -> LangCode:
    if ui_lang_code is not None and ui_lang_code in (lang.lang_code for lang in await get_all_ui_langs(db_session)): return ui_lang_code
    result: ScalarResult = await db_session.scalars(
        select(LanguageModel.code).where(LanguageModel.abbreviation == DEFAULT_UI_LANGUAGE)
    )
    lang_code: LangCode = result.one()
    return lang_code

UILangCode = Annotated[LangCode, Depends(ui_lang)]


@db_checker()
@cache(expire=3600)
async def get_all_ui_langs(db_session: DBSession) -> List[LanguageSchema]:
    result: ScalarResult = await db_session.scalars(
        select(LanguageModel)
        .where(LanguageModel.is_ui_lang == True)
        .order_by(LanguageModel.value)
    )
    lang_list = []
    for lang in result.all():
        lang_list.append(
            LanguageSchema(
                lang_code=lang.code,
                abbreviation=lang.abbreviation,
                lang_value=lang.value,
                is_ui_lang=lang.is_ui_lang,
            )
        )
    if not lang_list: raise CommonExceptions.NOTHING_FOUND
    return lang_list


@db_checker()
async def get_all_langs(db_session: DBSession) -> List[LanguageSchema]:
    result: ScalarResult = await db_session.scalars(
        select(LanguageModel)
        .order_by(LanguageModel.value)
    )
    lang_list = []
    for lang in result.all():
        lang_list.append(
            LanguageSchema(
                lang_code=lang.code,
                abbreviation=lang.abbreviation,
                lang_value=lang.value,
                is_ui_lang=lang.is_ui_lang
            )
        )
    if not lang_list: raise CommonExceptions.NOTHING_FOUND
    return lang_list
