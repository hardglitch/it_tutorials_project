from typing import List
from sqlalchemy import Result, Row, ScalarResult, and_, delete, distinct, func, select, update
from ...common.exceptions import CommonExceptions
from ...common.responses import CommonResponses, ResponseSchema
from ...db import DBSession
from ...dictionary.models import DictionaryModel
from ...dictionary.schemas import DictionarySchema
from ...language.schemas import LangCode
from ...tools import db_checker
from ...tutorial.dist_type.models import DistTypeModel
from ...tutorial.dist_type.schemas import DistTypeCode, DistTypeSchema


@db_checker()
async def add_dist_type(dist_type: DictionarySchema, db_session: DBSession) -> ResponseSchema:
    if not dist_type.word_code:
        result: ScalarResult = await db_session.scalars(func.max(DictionaryModel.word_code))
        max_word_code: int | None = result.one_or_none()
        dist_type.word_code = max_word_code + 1 if max_word_code else 1

    new_word = DictionaryModel(
        word_code=dist_type.word_code,
        lang_code=dist_type.lang_code,
        value=dist_type.dict_value,
    )
    db_session.add(new_word)
    await db_session.commit()
    await db_session.refresh(new_word)

    new_dist_type = DistTypeModel(
        word_code=new_word.word_code
    )
    db_session.add(new_dist_type)
    await db_session.commit()
    return CommonResponses.CREATED


@db_checker()
async def edit_dist_type(dist_type: DistTypeSchema, db_session: DBSession) -> ResponseSchema:
    result: ScalarResult = await db_session.scalars(
        select(DistTypeModel.word_code).where(dist_type.dist_type_code == DistTypeModel.code)
    )
    word_code: int = result.one()

    await db_session.execute(
        update(DictionaryModel)
        .where(and_(DictionaryModel.word_code == word_code, DictionaryModel.lang_code == dist_type.lang_code))
        .values(value=dist_type.dict_value)
    )
    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def delete_dist_type(dist_type_code: DistTypeCode, db_session: DBSession) -> ResponseSchema:
    dist_type_from_db: DistTypeModel | None = await db_session.get(DistTypeModel, dist_type_code)
    if not dist_type_from_db: raise CommonExceptions.NOTHING_FOUND

    # delete entry in the 'dictionary' table
    await db_session.execute(
        delete(DictionaryModel)
        .where(DictionaryModel.word_code == dist_type_from_db.word_code)
    )

    # delete entry in the 'distribution type' table
    await db_session.delete(dist_type_from_db)

    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def get_dist_type(dist_type_code: DistTypeCode, ui_lang_code: LangCode, db_session: DBSession) -> DistTypeSchema:
    result: Result = await db_session.execute(
        select(DistTypeModel.code, DictionaryModel.value)
        .where(and_(
            DistTypeModel.code == dist_type_code,
            DistTypeModel.word_code == DictionaryModel.word_code,
            DictionaryModel.lang_code == ui_lang_code,
        ))
    )

    dist_type: Row = result.one()
    return DistTypeSchema(
        dist_type_code=dist_type.code,
        dict_value=dist_type.value,
    )


@db_checker()
async def get_all_dist_types(ui_lang_code: LangCode, db_session: DBSession) -> List[DistTypeSchema]:
    result: Result = await db_session.execute(
        select(DistTypeModel.code, DictionaryModel.value)
        .distinct(DictionaryModel.value)
        .where(DistTypeModel.word_code == DictionaryModel.word_code, DictionaryModel.lang_code == ui_lang_code)
        .order_by(DictionaryModel.value)
    )

    dist_type_list = []
    for row in result.all():
        dist_type_list.append(
            DistTypeSchema(
                dist_type_code=row.code,
                dict_value=row.value
            )
        )
    if not dist_type_list: raise CommonExceptions.NOTHING_FOUND
    return dist_type_list
