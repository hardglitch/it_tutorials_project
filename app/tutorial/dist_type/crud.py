from typing import Annotated, List
from sqlalchemy import Result, Row, ScalarResult, and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import CommonExceptions
from app.common.responses import CommonResponses, ResponseSchema
from app.dictionary.models import DictionaryModel
from app.dictionary.schemas import AddWordToDictionarySchema, EditDictionarySchema
from app.tools import db_checker
from app.tutorial.dist_type.models import DistTypeModel
from app.tutorial.dist_type.schemas import DistTypeCodeSchema, GetTutorialDistTypeSchema


Code = Annotated[int, DistTypeCodeSchema]


@db_checker()
async def add_distribution_type(dist_type: AddWordToDictionarySchema, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        result: ScalarResult = await session.scalars(func.max(DictionaryModel.word_code))
        max_word_code: int | None = result.one_or_none()
        word_code = max_word_code + 1 if max_word_code else 1

        new_word = DictionaryModel(
            word_code=word_code,
            lang_code=dist_type.lang_code,
            value=dist_type.value,
        )
        session.add(new_word)
        await session.commit()
        await session.refresh(new_word)

        new_dist_type = DistTypeModel(
            word_code=new_word.word_code
        )
        session.add(new_dist_type)
        await session.commit()
        return CommonResponses.CREATED


@db_checker()
async def edit_distribution_type(dist_type: EditDictionarySchema, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        await session.execute(
            update(DictionaryModel)
            .where(and_(DictionaryModel.word_code == dist_type.word_code, DictionaryModel.lang_code == dist_type.lang_code))
            .values(value=dist_type.value)
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def delete_distribution_type(code: Code, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        dist_type_from_db: DistTypeModel | None = await session.get(DistTypeModel, code)
        if not dist_type_from_db: raise CommonExceptions.NOTHING_FOUND

        # delete entry in the 'dictionary' table
        await session.execute(
            delete(DictionaryModel)
            .where(DictionaryModel.word_code == dist_type_from_db.word_code)
        )

        # delete entry in the 'distribution type' table
        await session.delete(dist_type_from_db)

        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def get_distribution_type(code: Code, db_session: AsyncSession) -> GetTutorialDistTypeSchema:
    async with db_session as session:
        result: Result = await session.execute(
            select(DistTypeModel.code, DictionaryModel.value)
            .where(and_(
                DistTypeModel.code == code,
                DistTypeModel.word_code == DictionaryModel.word_code
            ))
        )

        dist_type: Row = result.one()
        return GetTutorialDistTypeSchema(
            dist_type_code=dist_type.code,
            dist_type_value=dist_type.value,
        )


@db_checker()
async def get_all_distribution_types(db_session: AsyncSession) -> List[GetTutorialDistTypeSchema]:
    async with db_session as session:
        result: Result = await session.execute(
            select(DistTypeModel.code, DictionaryModel.value)
            .where(DistTypeModel.word_code == DictionaryModel.word_code)
            .order_by(DictionaryModel.value)
        )

        dist_type_list = []
        for row in result.all():
            dist_type_list.append(
                GetTutorialDistTypeSchema(
                    dist_type_code=row.code,
                    dist_type_value=row.value
                )
            )
        if not dist_type_list: raise CommonExceptions.NOTHING_FOUND
        return dist_type_list
