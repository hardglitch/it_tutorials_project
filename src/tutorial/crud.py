from typing import Annotated
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.exceptions import TutorialExceptions
from src.constants.responses import CommonResponses, ResponseScheme, TutorialResponses
from src.language.crud import get_language
from src.language.schemas import LanguageScheme
from src.tools import db_checker, parameter_checker
from src.tutorial.dist_type.crud import get_distribution_type
from src.tutorial.dist_type.schemas import GetTutorialDistributionTypeScheme
from src.tutorial.models import Tutorial
from src.tutorial.schemas import AddTutorialScheme, EditTutorialScheme, GetTutorialScheme, TutorialIDScheme
from src.tutorial.theme.crud import get_theme
from src.tutorial.theme.schemas import GetTutorialThemeScheme
from src.tutorial.type.crud import get_tutorial_type
from src.tutorial.type.schemas import GetTutorialTypeScheme
from src.user.crud import get_user
from src.user.schemas import GetUserScheme


TutorID = Annotated[int, TutorialIDScheme]


@db_checker()
async def add_tutorial(tutor: AddTutorialScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        new_tutor = Tutorial(
            title=tutor.title,               # regexp
            type_code=tutor.type,
            theme_code=tutor.theme,
            description=tutor.description,   # regexp
            language_code=tutor.language,
            source_link=str(tutor.source_link),
            dist_type_code=tutor.dist_type,
            who_added_id=tutor.who_added
        )
        session.add(new_tutor)
        await session.commit()
        await session.refresh(new_tutor)
        return TutorialResponses.TUTORIAL_ADDED


@db_checker()
async def edit_tutorial(tutor_id: TutorID, tutor_data: EditTutorialScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        await session.execute(
            update(Tutorial)
            .where(Tutorial.id == tutor_id)
            .values(
                title=tutor_data.title,                #regexp
                type=tutor_data.type,
                theme=tutor_data.theme,
                language=tutor_data.language,
                description=tutor_data.description,    #regexp
                dist_type=tutor_data.dist_type,
                source_link=tutor_data.source_link
            )
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def delete_tutorial(tutor_id: TutorID, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        await session.delete(
            select(Tutorial)
            .where(Tutorial.id == tutor_id)
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def get_tutorial(tutor_id: TutorID, db_session: AsyncSession) -> AddTutorialScheme:
    async with db_session as session:
        tutor: AddTutorialScheme | None = await session.get(Tutorial, tutor_id)
        if not tutor: raise TutorialExceptions.TUTORIAL_NOT_FOUND
        return tutor


# All decoding operations will be on the client-side
@parameter_checker()
async def get_decoded_tutorial(tutor_id: TutorID, db_session: AsyncSession) -> GetTutorialScheme:
    tutor: Tutorial | AddTutorialScheme = await get_tutorial(tutor_id, db_session)

    decoded_type: GetTutorialTypeScheme = await get_tutorial_type(tutor.type_code, db_session)
    decoded_theme: GetTutorialThemeScheme = await get_theme(tutor.theme_code, db_session)
    decoded_lang: LanguageScheme = await get_language(tutor.language_code, db_session)
    decoded_dist_type: GetTutorialDistributionTypeScheme = await get_distribution_type(tutor.dist_type_code, db_session)
    decoded_user: GetUserScheme = await get_user(tutor.who_added_id, db_session)

    return GetTutorialScheme(
        title=tutor.title,
        type=decoded_type.value,
        theme=decoded_theme.value,
        language=decoded_lang.value,
        description=tutor.description,
        dist_type=decoded_dist_type.dist_type_value,
        source_link=tutor.source_link,
        who_added=decoded_user.name,
    )
