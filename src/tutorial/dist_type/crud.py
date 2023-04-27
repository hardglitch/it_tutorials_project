from typing import Annotated, List
from fastapi import Path
from sqlalchemy import Result, ScalarResult, delete, func, select, update
from sqlalchemy.exc import IntegrityError
from src.db import DBSession
from src.dictionary.models import Dictionary
from src.dictionary.schemas import AddWordToDictionaryScheme, EditDictionaryScheme
from src.tutorial.dist_type.models import TutorialDistributionType
from src.tutorial.dist_type.schemas import ReadTutorialDistributionTypeScheme


Code = Annotated[int, Path(title="A Code of a Distribution Type")]


async def add_distribution_type(dist_type: AddWordToDictionaryScheme, db_session: DBSession) -> bool | None:
    if not dist_type or not db_session: return False

    async with db_session as session:
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


async def edit_distribution_type(dist_type: EditDictionaryScheme, db_session: DBSession) -> bool | None:
    if not dist_type or not db_session or not all([param is not None for param in dist_type]): return False

    async with db_session as session:
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
        code: Code,
        db_session: DBSession
) -> bool | None:

    if not code or not db_session: return None

    async with db_session as session:
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


async def get_all_distribution_types(db_session: DBSession) -> List[ReadTutorialDistributionTypeScheme] | None:
    if not db_session: return None

    async with db_session as session:
        try:
            result: Result = await session.execute(
                select(TutorialDistributionType.code, Dictionary.value)
                .where(TutorialDistributionType.word_code == Dictionary.word_code)
                .order_by(Dictionary.value)
            )

            dist_type_list = []
            for res in result.all():
                dist_type_list.append(
                    ReadTutorialDistributionTypeScheme(
                        code=res.code,
                        value=res.value,
                    )
                )

        except IntegrityError:
            raise
