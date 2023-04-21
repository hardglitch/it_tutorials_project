from copy import deepcopy
from typing import Sequence
from fastapi import Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.constants import LANGUAGES, LanguageAbbreviation, UILanguage
from src.db import get_session
from src.language.schemas import EditLanguageScheme, LanguageScheme
from src.models import Language


@cache()
async def get_all_languages(async_session: AsyncSession = Depends(get_session)) -> None:
    async with async_session as session:
        try:
            result = await session.scalars(select(Language))
            langs: Sequence[LanguageScheme] = result.all()
            for lang in langs:
                setattr(LanguageAbbreviation, lang.abbreviation, lang.code)
                LANGUAGES[lang.code] = lang.value
                if lang.is_ui_lang: setattr(UILanguage, lang.abbreviation, lang.code)
        except Exception:
            raise


async def add_language(
        lang: LanguageScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool:

    if not lang: return False
    async with async_session as session:
        try:
            new_lang = Language(
                code=lang.code,
                abbreviation=lang.abbreviation,
                value=lang.value,
                is_ui_lang=lang.is_ui_lang
            )
            session.add(new_lang)
            await session.commit()
            return True

        except Exception:
            return False


async def edit_language(
        lang: EditLanguageScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    async with async_session as session:
        try:
            result = await session.scalars(
                select(Language).where(Language.code == lang.code)
            )
            lang_from_db: LanguageScheme = result.one_or_none()
            if not lang_from_db: return False

            lang_from_db_snapshot = deepcopy(lang_from_db)

            if lang.code and lang.code != lang_from_db.code:
                lang_from_db.code = lang.code
            if lang.abbreviation and lang.abbreviation != lang_from_db.abbreviation:
                lang_from_db.abbreviation = lang.abbreviation
            if lang.value and lang.value != lang_from_db.value:
                lang_from_db.value = lang.value
            if lang.is_ui_lang and lang.is_ui_lang != lang_from_db.is_ui_lang:
                lang_from_db.is_ui_lang = lang.is_ui_lang

            if lang_from_db.code != lang_from_db_snapshot.code or \
               lang_from_db.abbreviation != lang_from_db_snapshot.abbreviation or \
               lang_from_db.value != lang_from_db_snapshot.value or \
               lang_from_db.is_ui_lang != lang_from_db_snapshot.is_ui_lang:

                session.add(lang_from_db)
                await session.commit()
                return True
            else:
                return False

        except Exception:
            raise
