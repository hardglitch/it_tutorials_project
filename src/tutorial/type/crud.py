from typing import Annotated, List
from fastapi import Path
from sqlalchemy import Result, ScalarResult, delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.dictionary.models import Dictionary
from src.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from src.tutorial.type.models import TutorialType
from src.tutorial.type.schemas import ReadTutorialTypeScheme


async def get_all_tutorial_types(
        async_session: AsyncSession
) -> List[ReadTutorialTypeScheme] | None:

    if not async_session: return None

    async with async_session as session:
        try:
            result: Result = await session.execute(
                select(TutorialType.code, Dictionary.value)
                .where(TutorialType.word_code == Dictionary.word_code)
                .order_by(Dictionary.value)
            )

            tutor_type_list = []
            for res in result.all():
                tutor_type_list.append(
                    ReadTutorialTypeScheme(
                        type_code=res.code,
                        value=res.value,
                    )
                )

        except IntegrityError:
            raise


async def add_tutorial_type(
        tutor_type: AddWordToDictionaryScheme,
        async_session: AsyncSession
) -> bool | None:

    if not tutor_type or not async_session: return False

    async with async_session as session:
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

        except IntegrityError:
            raise
        except (TypeError, ValueError):
            return False


async def edit_tutorial_type(
        tutor_type: EditDictionaryScheme,
        async_session: AsyncSession
) -> bool | None:

    if not tutor_type or not async_session or not all([param is not None for param in tutor_type]): return False

    async with async_session as session:
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


async def delete_tutorial_type(
        code: Annotated[int, Path(title="A Code of a Distribution Type", ge=0)],
        async_session: AsyncSession
) -> bool | None:

    if not code or not async_session: return None

    async with async_session as session:
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

