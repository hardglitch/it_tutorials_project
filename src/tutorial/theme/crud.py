from typing import Annotated, List
from fastapi import Depends, Path
from sqlalchemy import Result, ScalarResult, delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.dictionary.models import Dictionary
from src.tutorial.theme.models import TutorialTheme
from src.tutorial.theme.schemas import AddTutorialThemeScheme, EditTutorialThemeScheme, GetTutorialThemeScheme


async def get_all_themes(
        async_session: AsyncSession = Depends(get_session)
) -> List[GetTutorialThemeScheme] | None:

    if not async_session: return None

    async with async_session as session:
        try:
            result: Result = await session.execute(
                select(TutorialTheme.code, TutorialTheme.type_code, Dictionary.value)
                .where(TutorialTheme.word_code == Dictionary.word_code)
                .order_by(Dictionary.value)
            )

            theme_list = []
            for res in result.all():
                theme_list.append(
                    GetTutorialThemeScheme(
                        theme_code=res.code,
                        value=res.value,
                        type_code=res.type_code
                    )
                )

        except IntegrityError:
            raise


async def add_theme(
        theme: AddTutorialThemeScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not theme or not async_session: return False

    async with async_session as session:
        try:
            result: ScalarResult = await session.scalars(func.max(Dictionary.word_code))
            max_word_code: int | None = result.one_or_none()
            word_code = max_word_code + 1 if max_word_code else 1

            new_word = Dictionary(
                word_code=word_code,
                lang_code=theme.lang_code,
                value=theme.value,
            )
            session.add(new_word)
            await session.commit()
            await session.refresh(new_word)

            new_dist_type = TutorialTheme(
                word_code=new_word.word_code,
                type_code=theme.type_code,
            )
            session.add(new_dist_type)
            await session.commit()
            return True

        except IntegrityError:
            raise
        except (TypeError, ValueError):
            return False


async def edit_theme(
        theme: EditTutorialThemeScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not theme or not async_session: return False

    async with async_session as session:
        try:
            # update word in the 'dictionary' table
            if theme.value.strip():
                await session.execute(
                    update(Dictionary)
                    .where(Dictionary.word_code == theme.word_code and Dictionary.lang_code == theme.lang_code)
                    .values(value=theme.value)
                )

            # update tutorial type code in the 'theme' table
            if theme.type_code is not None:
                await session.execute(
                    update(TutorialTheme)
                    .where(TutorialTheme.code == theme.theme_code)
                    .values(type_code=theme.type_code)
                )

            await session.commit()
            return True

        except Exception:
            raise


async def delete_theme(
        code: Annotated[int, Path(title="A Code of a Theme")],
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not code or not async_session: return None

    async with async_session as session:
        try:
            theme_from_db = await session.get(TutorialTheme, code)

            # delete record in the 'dictionary' table
            await session.execute(
                delete(Dictionary)
                .where(Dictionary.word_code == theme_from_db.word_code)
            )

            # delete record in the 'theme' table
            await session.delete(theme_from_db)

            await session.commit()
            return True

        except Exception:
            raise

