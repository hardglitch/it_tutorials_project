from typing import List
from sqlalchemy import Result, Row, ScalarResult, and_, delete, func, insert, select, update
from ...common.exceptions import CommonExceptions, DatabaseExceptions
from ...common.responses import CommonResponses, ResponseSchema
from ...db import DBSession
from ...dictionary.models import DictionaryModel
from ...dictionary.schemas import DictionarySchema
from ...language.schemas import LangCode
from ...tools import db_checker
from ...tutorial.type.models import TypeModel
from ...tutorial.type.schemas import TypeCode, TypeSchema


@db_checker()
async def add_type(tutor_type: DictionarySchema, db_session: DBSession) -> ResponseSchema:
    is_word_code: bool = True if tutor_type.word_code else False
    if not is_word_code:
        result: Result = await db_session.execute(
            select(DictionaryModel.lang_code, DictionaryModel.value)
        )
        for row in result.all():
            if row.lang_code == tutor_type.lang_code and row.value == tutor_type.dict_value:
                raise DatabaseExceptions.DUPLICATED_ENTRY

        result: ScalarResult = await db_session.scalars(func.max(DictionaryModel.word_code))
        max_word_code: int | None = result.one_or_none()
        tutor_type.word_code = max_word_code + 1 if max_word_code else 1

    new_word = DictionaryModel(
        word_code=tutor_type.word_code,
        lang_code=tutor_type.lang_code,
        value=tutor_type.dict_value,
    )
    db_session.add(new_word)
    await db_session.commit()

    if not is_word_code:
        await db_session.refresh(new_word)

        new_tutor_type = TypeModel(
            word_code=new_word.word_code
        )
        db_session.add(new_tutor_type)
        await db_session.commit()

    return CommonResponses.CREATED


@db_checker()
async def edit_type(tutor_type: TypeSchema, db_session: DBSession) -> ResponseSchema:
    result: ScalarResult = await db_session.scalars(
        select(TypeModel.word_code).where(tutor_type.type_code == TypeModel.code)
    )
    word_code: int = result.one()
    await db_session.merge(
        DictionaryModel(
            word_code=word_code,
            lang_code=tutor_type.lang_code,
            value=tutor_type.dict_value,
        )
    )
    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def delete_type(type_code: TypeCode, db_session: DBSession) -> ResponseSchema:
    tutor_type_from_db: TypeModel | None = await db_session.get(TypeModel, type_code)
    if not tutor_type_from_db: raise CommonExceptions.NOTHING_FOUND

    # delete entry in the 'dictionary' table
    await db_session.execute(
        delete(DictionaryModel)
        .where(DictionaryModel.word_code == tutor_type_from_db.word_code)
    )

    # delete entry in the 'type' table
    await db_session.delete(tutor_type_from_db)

    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def get_type(type_code: TypeCode, ui_lang_code: LangCode, db_session: DBSession) -> TypeSchema:
    result: Result = await db_session.execute(
        select(TypeModel.code, DictionaryModel.value)
        .where(and_(
            TypeModel.word_code == DictionaryModel.word_code,
            TypeModel.code == type_code,
            DictionaryModel.lang_code == ui_lang_code
        ))
    )

    type_: Row = result.one()
    return TypeSchema(
        type_code=type_.code,
        dict_value=type_.value,
    )


@db_checker()
async def get_all_types(db_session: DBSession, ui_lang_code: LangCode | None = None) -> List[TypeSchema]:
    result: Result = await db_session.execute(
        select(
            TypeModel.code,
            DictionaryModel.word_code,
            DictionaryModel.value,
            DictionaryModel.lang_code,
        )
        .where(
            and_(
                TypeModel.word_code == DictionaryModel.word_code,
                DictionaryModel.lang_code == ui_lang_code
            )
            if ui_lang_code else
                TypeModel.word_code == DictionaryModel.word_code
        )
        .order_by(DictionaryModel.value)
    )

    type_list = []
    for row in result.all():
        type_list.append(
            TypeSchema(
                type_code=row.code,
                dict_value=row.value,
                word_code=row.word_code,
                lang_code=row.lang_code,
            )
        )
    if not type_list: raise CommonExceptions.NOTHING_FOUND
    return type_list
