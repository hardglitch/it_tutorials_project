from typing import Annotated, List
from sqlalchemy import ScalarResult, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import CommonExceptions
from app.common.responses import CommonResponses, ResponseScheme
from app.language.models import Language
from app.language.schemas import EditLanguageScheme, LangCodeScheme, LanguageScheme
from app.tools import db_checker


LangCode = Annotated[int, LangCodeScheme]


@db_checker()
async def add_language(lang: LanguageScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        new_lang = Language(
            abbreviation=lang.abbreviation,
            value=lang.value,
            is_ui_lang=lang.is_ui_lang
        )
        session.add(new_lang)
        await session.commit()
        await session.refresh(new_lang)
        return CommonResponses.CREATED


@db_checker()
async def edit_language(lang: EditLanguageScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        await session.execute(
            update(Language)
            .where(Language.code == lang.lang_code)
            .values(
                abbreviation=lang.abbreviation,
                value=lang.value,
                is_ui_lang=lang.is_ui_lang
            )
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def delete_language(lang_code: LangCode, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        await session.delete(select(Language).where(Language.code == lang_code))
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def get_language(lang_code: LangCode, db_session: AsyncSession) -> LanguageScheme:
    async with db_session as session:
        lang_from_db: Language | None = await session.get(Language, lang_code)
        if not lang_from_db: raise CommonExceptions.NOTHING_FOUND
        return LanguageScheme(
            abbreviation=lang_from_db.abbreviation,
            value=lang_from_db.value,
            is_ui_lang=lang_from_db.is_ui_lang
        )


@db_checker()
async def get_all_languages(db_session: AsyncSession) -> List[EditLanguageScheme]:
    async with db_session as session:
        result: ScalarResult = await session.scalars(
            select(Language)
            .order_by(Language.value)
        )

        lang_list = []
        for row in result.all():
            lang_list.append(
                EditLanguageScheme(
                    lang_code=row.code,
                    abbreviation=row.abbreviation,
                    value=row.value,
                    is_ui_lang=row.is_ui_lang
                )
            )
        if not lang_list: raise CommonExceptions.NOTHING_FOUND
        return lang_list
