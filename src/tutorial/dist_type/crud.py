from typing import Annotated, List
from fastapi import Depends, Path
from sqlalchemy import Result, ScalarResult, delete, func, join, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.dictionary.models import Dictionary
from src.dictionary.schemas import DictionaryScheme
from src.tutorial.dist_type.models import TutorialDistributionType
from src.tutorial.dist_type.schemas import ReadTutorialDistributionTypeScheme


async def get_all_distribution_types(
        async_session: AsyncSession = Depends(get_session)
) -> List[ReadTutorialDistributionTypeScheme] | None:

    if not async_session: return None

    async with async_session as session:
        try:
            # SELECT code, value FROM distribution_type dt, dictionary d WHERE dt.word_code = d.word_code;
            result: Result = await session.execute(
                select(TutorialDistributionType.code, Dictionary.value)
                .where(TutorialDistributionType.word_code == Dictionary.word_code)
            )

            dist_type_list = list()
            for res in result.all():
                dist_type_list.append(
                    ReadTutorialDistributionTypeScheme(
                        code=res.code,
                        value=res.value,
                    )
                )

        except IntegrityError:
            raise


async def add_distribution_type(
        dist_type: DictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not dist_type or not async_session: return False

    async with async_session as session:
        try:
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
            return True

        except IntegrityError:
            raise
        except (TypeError, ValueError):
            return False


async def edit_distribution_type(
        dist_type: DictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not dist_type or not async_session or not all([param is not None for param in dist_type]): return False

    async with async_session as session:
        try:
            await session.execute(
                update(Dictionary)
                .where(Dictionary.word_code == dist_type.word_code and Dictionary.lang_code == dist_type.lang_code)
                .values(value=dist_type.value)
            )
            await session.commit()
            return True

        except Exception:
            raise


async def delete_distribution_type(
        code: Annotated[int, Path(title="A Code of a Distribution Type")],
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not code or not async_session: return None

    async with async_session as session:
        try:
            dist_type_from_db = await session.get(TutorialDistributionType, code)

            # delete record in the 'dictionary' table
            await session.execute(
                delete(Dictionary)
                .where(Dictionary.word_code == dist_type_from_db.word_code)
            )

            # delete record in the 'distribution type' table
            await session.delete(dist_type_from_db)

            await session.commit()
            return True

        except Exception:
            raise

