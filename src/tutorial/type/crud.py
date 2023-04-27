from typing import Annotated, List
from sqlalchemy import Result, ScalarResult, and_, delete, func, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from src.dictionary.models import Dictionary
from src.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from src.tutorial.type.models import TutorialType
from src.tutorial.type.schemas import GetTutorialTypeScheme, TypeCodeScheme


Code = Annotated[int, TypeCodeScheme]


async def add_tutorial_type(tutor_type: AddWordToDictionaryScheme, db_session: AsyncSession) -> bool | None:
    if not tutor_type or not db_session: return False

    async with db_session as session:
        try:
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
            return True

        except (TypeError, ValueError):
            return False
        except IntegrityError:
            raise


async def edit_tutorial_type(tutor_type: EditDictionaryScheme, db_session: AsyncSession) -> bool | None:
    if not tutor_type or not db_session or not all([param is not None for param in tutor_type]): return False

    async with db_session as session:
        try:
            await session.execute(
                update(Dictionary)
                .where(Dictionary.word_code == tutor_type.word_code and Dictionary.lang_code == tutor_type.lang_code)
                .values(value=tutor_type.value)
            )
            await session.commit()
            return True

        except IntegrityError:
            raise


async def delete_tutorial_type(code: Code, db_session: AsyncSession) -> bool | None:
    if not code or not db_session: return None

    async with db_session as session:
        try:
            tutor_type_from_db = await session.get(TutorialType, code)

            # delete record in the 'dictionary' table
            await session.execute(
                delete(Dictionary)
                .where(Dictionary.word_code == tutor_type_from_db.word_code)
            )

            # delete record in the 'type' table
            await session.delete(tutor_type_from_db)

            await session.commit()
            return True

        except IntegrityError:
            raise


async def get_tutorial_type(code: Code, db_session: AsyncSession) -> GetTutorialTypeScheme | None:
    if not code or not db_session: return None

    async with db_session as session:
        try:
            result: Result = await session.execute(
                select(TutorialType.code, Dictionary.value)
                .where(and_(TutorialType.word_code == Dictionary.word_code, TutorialType.code == code))
            )

            row = result.one_or_none()
            return GetTutorialTypeScheme(
                type_code=row.code,
                value=row.value,
            ) if row and row.code and row.value else None

        except NoResultFound:
            return None
        except IntegrityError:
            raise


async def get_all_tutorial_types(db_session: AsyncSession) -> List[GetTutorialTypeScheme] | None:
    if not db_session: return None

    async with db_session as session:
        try:
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
            return tutor_type_list if tutor_type_list else None

        except NoResultFound:
            return None
        except IntegrityError:
            raise
