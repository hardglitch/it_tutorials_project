from typing import Annotated, List
from sqlalchemy import Result, Row, ScalarResult, and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import CommonExceptions
from app.common.responses import CommonResponses, ResponseScheme
from app.dictionary.models import Dictionary
from app.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from app.tools import db_checker
from app.tutorial.type.models import TutorialType
from app.tutorial.type.schemas import GetTutorialTypeScheme, TypeCodeScheme


Code = Annotated[int, TypeCodeScheme]


@db_checker()
async def add_tutorial_type(tutor_type: AddWordToDictionaryScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        result: ScalarResult = await session.scalars(func.max(Dictionary.word_code))
        max_word_code: int | None = result.one_or_none()
        word_code = max_word_code + 1 if max_word_code else 1

        new_word = Dictionary(
            word_code=word_code,
            lang_code=tutor_type.lang_code,
            value=tutor_type.value,
        )
        session.add(new_word)
        await session.commit()
        await session.refresh(new_word)

        new_tutor_type = TutorialType(
            word_code=new_word.word_code
        )
        session.add(new_tutor_type)
        await session.commit()
        return CommonResponses.CREATED


@db_checker()
async def edit_tutorial_type(tutor_type: EditDictionaryScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        await session.execute(
            update(Dictionary)
            .where(Dictionary.word_code == tutor_type.word_code and Dictionary.lang_code == tutor_type.lang_code)
            .values(value=tutor_type.value)
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def delete_tutorial_type(code: Code, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        tutor_type_from_db: TutorialType | None = await session.get(TutorialType, code)
        if not tutor_type_from_db: raise CommonExceptions.NOTHING_FOUND

        # delete entry in the 'dictionary' table
        await session.execute(
            delete(Dictionary)
            .where(Dictionary.word_code == tutor_type_from_db.word_code)
        )

        # delete entry in the 'type' table
        await session.delete(tutor_type_from_db)

        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def get_tutorial_type(code: Code, db_session: AsyncSession) -> GetTutorialTypeScheme:
    async with db_session as session:
        result: Result = await session.execute(
            select(TutorialType.code, Dictionary.value)
            .where(and_(TutorialType.word_code == Dictionary.word_code, TutorialType.code == code))
        )

        row: Row = result.one()
        return GetTutorialTypeScheme(
            type_code=row.code,
            value=row.value,
        )


@db_checker()
async def get_all_tutorial_types(db_session: AsyncSession) -> List[GetTutorialTypeScheme]:
    async with db_session as session:
        result: Result = await session.execute(
            select(TutorialType.code, Dictionary.value)
            .where(TutorialType.word_code == Dictionary.word_code)
            .order_by(Dictionary.value)
        )

        tutor_type_list = []
        for row in result.all():
            tutor_type_list.append(
                GetTutorialTypeScheme(
                    type_code=row.code,
                    value=row.value,
                )
            )
        if not tutor_type_list: raise CommonExceptions.NOTHING_FOUND
        return tutor_type_list
