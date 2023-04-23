from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.constants.responses import TutorialResponses
from src.tutorial.models import Tutorial
from src.tutorial.schemas import TutorialScheme
from src.tutorial.theme.models import TutorialTheme
from src.tutorial.type.models import TutorialType


async def create_tutorial(
        tutorial: TutorialScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not tutorial or not async_session or not all([param is not None for param in tutorial]):
        return TutorialResponses.PARAMETER_ERRORS

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
                who_added_id=tutorial.who_added
            )
            session.add(new_tutorial)
            await session.commit()
            return TutorialResponses.TUTORIAL_ADDED

        except IntegrityError:
            return TutorialResponses.TUTORIAL_ALREADY_EXISTS


async def get_tutorial_from_db(
        tutorial_id: int,
        async_session: AsyncSession = Depends(get_session)
) -> Tutorial | None:

    if not tutorial_id or not async_session: return None
    async with async_session as session:
        try:
            return await session.get(Tutorial, tutorial_id)
        except Exception:
            raise


# ------------- THEME ----------------

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


async def delete_tutorial_theme(tutor_theme: TutorialTheme, async_session: AsyncSession = Depends(get_session)):
    pass

# ------------- TYPE ----------------


async def add_tutorial_type(tutor_type: TutorialType, async_session: AsyncSession = Depends(get_session)):
    async with async_session as session:
        try:
            session.add(tutor_type)
            await session.commit()
            await session.refresh(tutor_type)
        except Exception:
            raise


async def edit_tutorial_type(tutor_type: TutorialType, async_session: AsyncSession = Depends(get_session)):
    async with async_session as session:
        try:
            session.add(tutor_type)
            await session.commit()
            await session.refresh(tutor_type)
        except Exception:
            raise


async def delete_tutorial_type(tutor_type: TutorialType, async_session: AsyncSession = Depends(get_session)):
    async with async_session as session:
        try:
            session.add(tutor_type)
            await session.commit()
            await session.refresh(tutor_type)
        except Exception:
            raise
