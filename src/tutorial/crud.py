from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.responses import ResponseScheme, TutorialResponses
from src.tools import db_checker
from src.tutorial.models import Tutorial
from src.tutorial.schemas import TutorialScheme


@db_checker()
async def add_tutorial(tutorial: TutorialScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        new_tutorial = Tutorial(
            title=tutorial.title,
            type=tutorial.type,
            theme=tutorial.theme,
            description=tutorial.description,
            language=tutorial.language,
            source_link=tutorial.source_link,
            dist_type=tutorial.dist_type,
            who_added_id=tutorial.who_added
        )
        session.add(new_tutorial)
        await session.commit()
        await session.refresh(new_tutorial)
        return TutorialResponses.TUTORIAL_ADDED
