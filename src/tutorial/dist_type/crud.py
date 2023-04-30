from typing import Annotated, List
from sqlalchemy import Result, Row, ScalarResult, and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants.exceptions import CommonExceptions
from src.constants.responses import CommonResponses, ResponseScheme
from src.dictionary.models import Dictionary
from src.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from src.tools import db_checker
from src.tutorial.dist_type.models import TutorialDistributionType
from src.tutorial.dist_type.schemas import DistTypeCodeScheme, GetTutorialDistributionTypeScheme


Code = Annotated[int, DistTypeCodeScheme]


@db_checker()
async def add_distribution_type(dist_type: AddWordToDictionaryScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        result: ScalarResult = await session.scalars(func.max(Dictionary.word_code))
        max_word_code: int | None = result.one_or_none()
        word_code = max_word_code + 1 if max_word_code else 1

        new_word = Dictionary(
            word_code=word_code,
            lang_code=dist_type.lang_code,
            value=dist_type.value,
        )
        session.add(new_word)
        await session.commit()
        await session.refresh(new_word)

        new_dist_type = TutorialDistributionType(
            word_code=new_word.word_code
        )
        session.add(new_dist_type)
        await session.commit()
        return CommonResponses.CREATED


@db_checker()
async def edit_distribution_type(dist_type: EditDictionaryScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        await session.execute(
            update(Dictionary)
            .where(and_(Dictionary.word_code == dist_type.word_code, Dictionary.lang_code == dist_type.lang_code))
            .values(value=dist_type.value)
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def delete_distribution_type(code: Code, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        dist_type_from_db = await session.get(TutorialDistributionType, code)

        # delete entry in the 'dictionary' table
        await session.execute(
            delete(Dictionary)
            .where(Dictionary.word_code == dist_type_from_db.word_code)
        )

        # delete entry in the 'distribution type' table
        await session.delete(dist_type_from_db)

        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def get_distribution_type(code: Code, db_session: AsyncSession) -> GetTutorialDistributionTypeScheme:
    async with db_session as session:
        result: Result = await session.execute(
            select(TutorialDistributionType.code, Dictionary.value)
            .where(and_(
                TutorialDistributionType.code == code,
                TutorialDistributionType.word_code == Dictionary.word_code
            ))
        )

        dist_type: Row = result.one_or_none()
        return GetTutorialDistributionTypeScheme(
            dist_type_code=dist_type.code,
            dist_type_value=dist_type.value,
        )


@db_checker()
async def get_all_distribution_types(db_session: AsyncSession) -> List[GetTutorialDistributionTypeScheme]:
    async with db_session as session:
        result: Result = await session.execute(
            select(TutorialDistributionType.code, Dictionary.value)
            .where(TutorialDistributionType.word_code == Dictionary.word_code)
            .order_by(Dictionary.value)
        )

        dist_type_list = []
        for row in result.all():
            dist_type_list.append(
                GetTutorialDistributionTypeScheme(
                    dist_type_code=row.code,
                    dist_type_value=row.value
                )
            )
        if not dist_type_list: raise CommonExceptions.NOTHING_FOUND
        return dist_type_list
