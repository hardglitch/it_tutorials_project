from typing import Annotated, List
from sqlalchemy import Result, Row, ScalarResult, and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import CommonExceptions
from app.common.responses import CommonResponses, ResponseSchema
from app.dictionary.models import DictionaryModel
from app.tools import db_checker
from app.tutorial.theme.models import ThemeModel
from app.tutorial.theme.schemas import AddTutorialThemeSchema, EditTutorialThemeSchema, GetTutorialThemeSchema, \
    ThemeCodeSchema


Code = Annotated[int, ThemeCodeSchema]


@db_checker()
async def add_theme(theme: AddTutorialThemeSchema, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        result: ScalarResult = await session.scalars(func.max(DictionaryModel.word_code))
        max_word_code: int | None = result.one_or_none()
        word_code = max_word_code + 1 if max_word_code else 1

        new_word = DictionaryModel(
            word_code=word_code,
            lang_code=theme.lang_code,
            value=theme.value
        )
        session.add(new_word)
        await session.commit()
        await session.refresh(new_word)

        new_dist_type = ThemeModel(
            word_code=new_word.word_code,
            type_code=theme.type_code
        )
        session.add(new_dist_type)
        await session.commit()
        return CommonResponses.CREATED


@db_checker()
async def edit_theme(theme: EditTutorialThemeSchema, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        # update word in the 'dictionary' table
        if theme.value:
            await session.execute(
                update(DictionaryModel)
                .where(DictionaryModel.word_code == theme.word_code and DictionaryModel.lang_code == theme.lang_code)
                .values(value=theme.value)
            )

        # update tutorial type code in the 'theme' table
        if theme.type_code is not None:
            await session.execute(
                update(ThemeModel)
                .where(ThemeModel.code == theme.theme_code)
                .values(type_code=theme.type_code)
            )

        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def delete_theme(code: Code, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        theme_from_db: ThemeModel | None = await session.get(ThemeModel, code)
        if not theme_from_db: raise CommonExceptions.NOTHING_FOUND

        # delete entry in the 'dictionary' table
        await session.execute(
            delete(DictionaryModel)
            .where(DictionaryModel.word_code == theme_from_db.word_code)
        )

        # delete entry in the 'theme' table
        await session.delete(theme_from_db)

        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def get_theme(code: Code, db_session: AsyncSession) -> GetTutorialThemeSchema:
    async with db_session as session:
        result: Result = await session.execute(
            select(ThemeModel.code, ThemeModel.type_code, ThemeModel.word_code, DictionaryModel.value)
            .where(and_(ThemeModel.code == code, ThemeModel.word_code == DictionaryModel.word_code))
        )

        row: Row = result.one()
        return GetTutorialThemeSchema(
            theme_code=row.code,
            value=row.value,
            type_code=row.type_code,
            word_code=row.word_code
        )


@db_checker()
async def get_all_themes(db_session: AsyncSession) -> List[GetTutorialThemeSchema]:
    async with db_session as session:
        result: Result = await session.execute(
            select(ThemeModel.code, ThemeModel.type_code, ThemeModel.word_code, DictionaryModel.value)
            .where(ThemeModel.word_code == DictionaryModel.word_code)
            .order_by(DictionaryModel.value)
        )

        theme_list = []
        for row in result.all():
            theme_list.append(
                GetTutorialThemeSchema(
                    theme_code=row.code,
                    value=row.value,
                    type_code=row.type_code,
                    word_code=row.word_code
                )
            )
        if not theme_list: raise CommonExceptions.NOTHING_FOUND
        return theme_list
