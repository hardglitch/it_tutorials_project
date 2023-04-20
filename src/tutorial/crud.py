from fastapi import Depends
from sqlalchemy import Result, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.constants.constants import LANGUAGES, LanguageAbbreviation, ShareType, TUTORIAL_THEMES, TUTORIAL_TYPES
from src.models import Tutorial, TutorialTheme, TutorialType
from src.constants.responses import TutorialResponses
from src.tutorial.schemas import DecryptedTutorialScheme, TutorialScheme


async def create_tutorial(
        tutorial: TutorialScheme,
        user_id: int,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    async with async_session as session:
        try:
            new_tutorial = Tutorial(
                title=tutorial.title,
                type=tutorial.type,
                theme=tutorial.theme,
                description=tutorial.description,
                language=tutorial.language,
                source_link=tutorial.source_link,
                share_type=tutorial.share_type,
                who_added_id=user_id
            )
            session.add(new_tutorial)
            await session.commit()
            await session.refresh(new_tutorial)
            return TutorialResponses.TUTORIAL_CREATED
        except IntegrityError:
            return TutorialResponses.TUTORIAL_ALREADY_EXISTS


async def get_tutorial_from_db(
        tutorial_id: int,
        async_session: AsyncSession = Depends(get_session)
) -> Tutorial | None:

    async with async_session as session:
        try:
            return await session.get(Tutorial, tutorial_id)
        except Exception:
            raise


def decrypt_tutorial(tutor: Tutorial | TutorialScheme) -> DecryptedTutorialScheme:
    return DecryptedTutorialScheme(
        title=tutor.title,
        type=TUTORIAL_TYPES[tutor.type],
        theme=TUTORIAL_THEMES[tutor.theme],
        description=tutor.description,
        language=LANGUAGES[tutor.language],
        source_link=tutor.source_link,
        share_type=ShareType(tutor.share_type).name
    )


async def add_tutorial_theme(tutor_theme: TutorialTheme, async_session: AsyncSession = Depends(get_session)):
    async with async_session as session:
        try:
            session.add(tutor_theme)
            await session.commit()
            await session.refresh(tutor_theme)
        except Exception:
            raise


async def edit_tutorial_theme(tutor_theme: TutorialTheme, async_session: AsyncSession = Depends(get_session)):
    async with async_session as session:
        try:
            session.add(tutor_theme)
            await session.commit()
            await session.refresh(tutor_theme)
        except Exception:
            raise


async def add_tutorial_type(tutor_type: TutorialType, async_session: AsyncSession = Depends(get_session)):
    async with async_session as session:
        try:
            session.add(tutor_type)
            await session.commit()
            await session.refresh(tutor_type)
        except Exception:
            raise


async def get_all_tutorial_themes_by_ui_language(
        ui_lang: int = 0,
        async_session: AsyncSession = Depends(get_session)
) -> None:
    async with async_session as session:
        try:
            result: Result = await session.execute(
                select(
                    TutorialTheme.id,
                    getattr(TutorialTheme, LanguageAbbreviation(ui_lang).name)
                )
            )
            res = result.fetchall()
            for row in res:
                TUTORIAL_THEMES[row[0]] = row[1]

        except Exception:
            raise


async def get_all_tutorial_types_by_ui_language(
        ui_lang: int = 0,
        async_session: AsyncSession = Depends(get_session)
) -> None:
    async with async_session as session:
        try:
            result: Result = await session.execute(
                select(
                    TutorialType.id,
                    getattr(TutorialType, LanguageAbbreviation(ui_lang).name)
                )
            )
            res = result.fetchall()
            for row in res:
                TUTORIAL_TYPES[row[0]] = row[1]

        except Exception:
            raise
