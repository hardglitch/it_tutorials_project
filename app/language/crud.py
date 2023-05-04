from typing import Annotated, List
from sqlalchemy import ScalarResult, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import CommonExceptions
from app.common.responses import CommonResponses, ResponseSchema
from app.language.models import LanguageModel
from app.language.schemas import EditLanguageSchema, LangCodeSchema, LanguageSchema
from app.tools import db_checker


LangCode = Annotated[int, LangCodeSchema]


@db_checker()
async def add_language(lang: LanguageSchema, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        new_lang = LanguageModel(
            abbreviation=lang.abbreviation,
            value=lang.value,
            is_ui_lang=lang.is_ui_lang
        )
        session.add(new_lang)
        await session.commit()
        await session.refresh(new_lang)
        return CommonResponses.CREATED


@db_checker()
async def edit_language(lang: EditLanguageSchema, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        await session.execute(
            update(LanguageModel)
            .where(LanguageModel.code == lang.lang_code)
            .values(
                abbreviation=lang.abbreviation,
                value=lang.value,
                is_ui_lang=lang.is_ui_lang
            )
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def delete_language(lang_code: LangCode, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        await session.delete(select(LanguageModel).where(LanguageModel.code == lang_code))
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def get_language(lang_code: LangCode, db_session: AsyncSession) -> LanguageSchema:
    async with db_session as session:
        lang_from_db: LanguageModel | None = await session.get(LanguageModel, lang_code)
        if not lang_from_db: raise CommonExceptions.NOTHING_FOUND
        return LanguageSchema(
            abbreviation=lang_from_db.abbreviation,
            value=lang_from_db.value,
            is_ui_lang=lang_from_db.is_ui_lang
        )


@db_checker()
async def get_all_languages(db_session: AsyncSession) -> List[EditLanguageSchema]:
    async with db_session as session:
        result: ScalarResult = await session.scalars(
            select(LanguageModel)
            .order_by(LanguageModel.value)
        )

        lang_list = []
        for row in result.all():
            lang_list.append(
                EditLanguageSchema(
                    lang_code=row.code,
                    abbreviation=row.abbreviation,
                    value=row.value,
                    is_ui_lang=row.is_ui_lang
                )
            )
        if not lang_list: raise CommonExceptions.NOTHING_FOUND
        return lang_list
