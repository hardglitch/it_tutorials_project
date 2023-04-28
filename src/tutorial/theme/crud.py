from typing import Annotated, List
from sqlalchemy import Result, Row, ScalarResult, and_, delete, func, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.exceptions import CommonExceptions
from src.constants.responses import CommonResponses, ResponseScheme
from src.dictionary.models import Dictionary
from src.tutorial.theme.models import TutorialTheme
from src.tutorial.theme.schemas import AddTutorialThemeScheme, EditTutorialThemeScheme, GetTutorialThemeScheme, \
    ThemeCodeScheme


Code = Annotated[int, ThemeCodeScheme]


async def add_theme(theme: AddTutorialThemeScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
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
            return CommonResponses.CREATED

        except (TypeError, ValueError):
            raise CommonExceptions.INVALID_PARAMETERS
        except IntegrityError:
            raise CommonExceptions.DUPLICATED_ENTRY


async def edit_theme(theme: EditTutorialThemeScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
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
            return CommonResponses.SUCCESS

        except (TypeError, ValueError):
            raise CommonExceptions.INVALID_PARAMETERS


async def delete_theme(code: Code, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        try:
            theme_from_db = await session.get(TutorialTheme, code)
            if not theme_from_db: raise CommonExceptions.NOTHING_FOUND

            # delete record in the 'dictionary' table
            await session.execute(
                delete(Dictionary)
                .where(Dictionary.word_code == theme_from_db.word_code)
            )

            # delete record in the 'theme' table
            await session.delete(theme_from_db)

            await session.commit()
            return CommonResponses.SUCCESS

        except (TypeError, ValueError):
            raise CommonExceptions.INVALID_PARAMETERS


async def get_theme(code: Code, db_session: AsyncSession) -> GetTutorialThemeScheme:
    async with db_session as session:
        try:
            result: Result = await session.execute(
                select(TutorialTheme.code, TutorialTheme.type_code, TutorialTheme.word_code, Dictionary.value)
                .where(and_(TutorialTheme.code == code, TutorialTheme.word_code == Dictionary.word_code))
            )

            row: Row = result.one_or_none()
            return GetTutorialThemeScheme(
                theme_code=row.code,
                value=row.value,
                type_code=row.type_code,
                word_code=row.word_code
            )

        except (ValueError, TypeError):
            raise CommonExceptions.INVALID_PARAMETERS
        except (NoResultFound, AttributeError):
            raise CommonExceptions.NOTHING_FOUND


async def get_all_themes(db_session: AsyncSession) -> List[GetTutorialThemeScheme]:
    async with db_session as session:
        try:
            result: Result = await session.execute(
                select(TutorialTheme.code, TutorialTheme.type_code, TutorialTheme.word_code, Dictionary.value)
                .where(TutorialTheme.word_code == Dictionary.word_code)
                .order_by(Dictionary.value)
            )

            theme_list = []
            for row in result.all():
                theme_list.append(
                    GetTutorialThemeScheme(
                        theme_code=row.code,
                        value=row.value,
                        type_code=row.type_code,
                        word_code=row.word_code
                    )
                )
            return theme_list if theme_list else None

        except NoResultFound:
            raise CommonExceptions.NOTHING_FOUND
        except (TypeError, ValueError):
            raise CommonExceptions.INVALID_PARAMETERS
