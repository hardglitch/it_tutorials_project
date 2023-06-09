from typing import List
from sqlalchemy import Result, Row, ScalarResult, and_, delete, func, select, update
from ..type.schemas import TypeCode
from ...common.exceptions import CommonExceptions, DatabaseExceptions
from ...common.responses import CommonResponses, ResponseSchema
from ...db import DBSession
from ...dictionary.models import DictionaryModel
from ...language.schemas import LangCode
from ...tools import db_checker
from ...tutorial.theme.models import ThemeModel
from ...tutorial.theme.schemas import ThemeSchema, ThemeCode


@db_checker()
async def add_theme(theme: ThemeSchema, db_session: DBSession) -> ResponseSchema:
    is_word_code: bool = True if theme.word_code else False
    if not is_word_code:
        result: Result = await db_session.execute(
            select(DictionaryModel.lang_code, DictionaryModel.value)
        )
        for row in result.all():
            if row.lang_code == theme.lang_code and row.value == theme.dict_value:
                raise DatabaseExceptions.DUPLICATED_ENTRY

        result: ScalarResult = await db_session.scalars(func.max(DictionaryModel.word_code))
        max_word_code: int | None = result.one_or_none()
        theme.word_code = max_word_code + 1 if max_word_code else 1

    new_word = DictionaryModel(
        word_code=theme.word_code,
        lang_code=theme.lang_code,
        value=theme.dict_value
    )
    db_session.add(new_word)
    await db_session.commit()

    if not is_word_code:
        await db_session.refresh(new_word)

        new_theme = ThemeModel(
            word_code=new_word.word_code,
            type_code=theme.type_code
        )
        db_session.add(new_theme)
        await db_session.commit()

    return CommonResponses.CREATED


@db_checker()
async def edit_theme(theme: ThemeSchema, db_session: DBSession) -> ResponseSchema:
    result: Result = await db_session.execute(
        select(DictionaryModel)
        .where(and_(
            ThemeModel.word_code == DictionaryModel.word_code,
            ThemeModel.code == theme.theme_code,
            DictionaryModel.lang_code == theme.lang_code
        ))
    )
    new_value: Row = result.one()
    new_value.DictionaryModel.value = theme.dict_value

    # update word in the 'dictionary' table
    await db_session.merge(new_value.DictionaryModel)

    # update tutorial type code in the 'theme' table
    if theme.type_code is not None:
        await db_session.execute(
            update(ThemeModel)
            .where(ThemeModel.code == theme.theme_code)
            .values(type_code=theme.type_code)
        )

    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def delete_theme(theme_code: ThemeCode, db_session: DBSession) -> ResponseSchema:
    theme_from_db: ThemeModel | None = await db_session.get(ThemeModel, theme_code)
    if not theme_from_db: raise CommonExceptions.NOTHING_FOUND

    # delete entry in the 'dictionary' table
    await db_session.execute(
        delete(DictionaryModel)
        .where(DictionaryModel.word_code == theme_from_db.word_code)
    )

    # delete entry in the 'theme' table
    await db_session.delete(theme_from_db)

    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def get_theme(theme_code: ThemeCode, ui_lang_code: LangCode, db_session: DBSession) -> ThemeSchema:
    result: Result = await db_session.execute(
        select(ThemeModel.code, ThemeModel.type_code, ThemeModel.word_code, DictionaryModel.value)
        .where(and_(
            ThemeModel.code == theme_code,
            ThemeModel.word_code == DictionaryModel.word_code),
            DictionaryModel.lang_code == ui_lang_code
        )
    )

    theme: Row = result.one()
    return ThemeSchema(
        theme_code=theme.code,
        dict_value=theme.value,
        type_code=theme.type_code,
    )


@db_checker()
async def get_all_themes(db_session: DBSession, ui_lang_code: LangCode | None = None) -> List[ThemeSchema]:
    result: Result = await db_session.execute(
        select(
            ThemeModel.code,
            ThemeModel.type_code,
            ThemeModel.word_code,
            DictionaryModel.value,
            DictionaryModel.lang_code,
        )
        .where(
            and_(
                ThemeModel.word_code == DictionaryModel.word_code,
                DictionaryModel.lang_code == ui_lang_code
            )
            if ui_lang_code else
                ThemeModel.word_code == DictionaryModel.word_code,
        )
        .order_by(DictionaryModel.value)
    )

    theme_list = []
    for theme in result.all():
        theme_list.append(
            ThemeSchema(
                theme_code=theme.code,
                dict_value=theme.value,
                type_code=theme.type_code,
                word_code=theme.word_code,
                lang_code=theme.lang_code,
            )
        )
    if not theme_list: raise CommonExceptions.NOTHING_FOUND
    return theme_list


@db_checker()
async def get_all_allowed_themes(
        type_code: TypeCode,
        ui_lang_code: LangCode,
        db_session: DBSession
) -> List[ThemeSchema]:

    result: Result = await db_session.execute(
        select(ThemeModel.code, ThemeModel.word_code, DictionaryModel.value)
        .where(and_(
            ThemeModel.type_code == type_code,
            ThemeModel.word_code == DictionaryModel.word_code,
            DictionaryModel.lang_code == ui_lang_code
        ))
        .order_by(DictionaryModel.value)
    )

    theme_list = []
    for theme in result.all():
        theme_list.append(
            ThemeSchema(
                theme_code=theme.code,
                dict_value=theme.value,
                type_code=theme.type_code,
                word_code=theme.word_code,
            )
        )
    if not theme_list: raise CommonExceptions.NOTHING_FOUND
    return theme_list
