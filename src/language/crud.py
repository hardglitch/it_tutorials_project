from typing import Annotated, List
from sqlalchemy import ScalarResult, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.exceptions import CommonExceptions
from src.language.models import Language
from src.language.schemas import EditLanguageScheme, LangCodeScheme, LanguageScheme


LangCode = Annotated[int, LangCodeScheme]


async def add_language(lang: LanguageScheme, db_session: AsyncSession) -> int:
    if not lang or not db_session: raise CommonExceptions.INVALID_PARAMETERS

    async with db_session as session:
        try:
            new_lang = Language(
                abbreviation=lang.abbreviation,
                value=lang.value,
                is_ui_lang=lang.is_ui_lang
            )
            session.add(new_lang)
            await session.commit()
            await session.refresh(new_lang)
            return new_lang.code

        except (TypeError, ValueError):
            raise CommonExceptions.INVALID_PARAMETERS
        except IntegrityError:
            raise CommonExceptions.DUPLICATED_ENTRY


async def edit_language(lang: EditLanguageScheme, db_session: AsyncSession) -> None:
    if not lang or not db_session: raise CommonExceptions.INVALID_PARAMETERS

    async with db_session as session:
        try:
            await session.execute(
                update(Language)
                .where(Language.code == lang.code)
                .values(
                    abbreviation=lang.abbreviation,
                    value=lang.value,
                    is_ui_lang=lang.is_ui_lang
                )
            )
            await session.commit()

        except (TypeError, ValueError):
            raise CommonExceptions.INVALID_PARAMETERS


async def delete_language(lang_code: LangCode, db_session: AsyncSession) -> None:
    if not lang_code or not db_session: raise CommonExceptions.INVALID_PARAMETERS

    async with db_session as session:
        try:
            lang = await session.get(Language, lang_code)
            await session.delete(lang)
            await session.commit()

        except (TypeError, ValueError):
            raise CommonExceptions.INVALID_PARAMETERS


async def get_language(lang_code: LangCode, db_session: AsyncSession) -> LanguageScheme:
    if not lang_code or not db_session: raise CommonExceptions.INVALID_PARAMETERS

    async with db_session as session:
        try:
            lang_from_db: LanguageScheme | None = await session.get(Language, lang_code)
            if not lang_from_db: raise CommonExceptions.NOTHING_FOUND
            return LanguageScheme(
                abbreviation=lang_from_db.abbreviation,
                value=lang_from_db.value,
                is_ui_lang=lang_from_db.is_ui_lang
            )

        except (TypeError, ValueError):
            raise CommonExceptions.INVALID_PARAMETERS


async def get_all_languages(db_session: AsyncSession) -> List[EditLanguageScheme]:
    if not db_session: raise CommonExceptions.INVALID_PARAMETERS

    async with db_session as session:
        try:
            result: ScalarResult = await session.scalars(
                select(Language)
                .order_by(Language.value)
            )

            lang_list = []
            for row in result.all():
                lang_list.append(
                    EditLanguageScheme(
                        code=row.code,
                        abbreviation=row.abbreviation,
                        value=row.value,
                        is_ui_lang=row.is_ui_lang
                    )
                )
            return lang_list

        except NoResultFound:
            raise CommonExceptions.NOTHING_FOUND
        except (TypeError, ValueError):
            raise CommonExceptions.INVALID_PARAMETERS
