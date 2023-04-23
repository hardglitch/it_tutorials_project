from typing import Annotated
from fastapi import Depends, Path
from sqlalchemy import ScalarResult, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.constants import Table
from src.db import get_session
from src.dictionary.models import Dictionary
from src.dictionary.schemas import DictionaryScheme
from src.tutorial.dist_type.models import TutorialDistributionType


async def add_distribution_type(
        dist_type: DictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not dist_type or not async_session or \
       not all([param is not None for param in dist_type]): return False

    async with async_session as session:
        try:
            result: ScalarResult = await session.scalars(
                text(f"SELECT MAX({Dictionary.word_code}) FROM {Table.Dictionary.table_name}"))
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


async def edit_distribution_type(
        dist_type: DictionaryScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not dist_type or not async_session or not all([param is not None for param in dist_type]): return False

    async with async_session as session:
        try:
            result = await session.execute(
                select(Dictionary)
                .where(Dictionary.word_code == dist_type.word_code and Dictionary.lang_code == dist_type.lang_code)
            )
            for row in result.one():
                new_dist_type = Dictionary(
                    word_code=row.word_code,
                    lang_code=row.lang_code,
                    value=dist_type.value,
                )

            session.add(new_dist_type)
            await session.commit()
            await session.refresh(new_dist_type)
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
            await session.delete(dist_type_from_db)
            await session.commit()
            return True

        except Exception:
            raise

