from typing import Dict
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.db_const import Language, ShareType
from src.models import Tutorial
from src.responses import TutorialResponses
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


async def get_tutorial_from_db(tutorial_id: int, async_session: AsyncSession = Depends(get_session)) -> Tutorial | None:
    async with async_session as session:
        try:
            return await session.get(Tutorial, tutorial_id)
        except Exception:
            raise


def decrypt_tutorial(tutor: Tutorial | TutorialScheme) -> DecryptedTutorialScheme:
    return DecryptedTutorialScheme(
        title=tutor.title,
        type=tutor.type,
        theme=tutor.theme,
        description=tutor.description,
        language=Language(tutor.language).name,
        source_link=tutor.source_link,
        share_type=ShareType(tutor.share_type).name
    )
