from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.constants.responses import TutorialResponses
from src.tutorial.models import Tutorial
from src.tutorial.schemas import TutorialScheme


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
