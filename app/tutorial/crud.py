from typing import Annotated
from pydantic import HttpUrl, parse_obj_as
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.responses import CommonResponses, ResponseScheme
from app.language.crud import get_language
from app.language.schemas import LanguageScheme
from app.tools import db_checker, parameter_checker
from app.tutorial.dist_type.crud import get_distribution_type
from app.tutorial.dist_type.schemas import GetTutorialDistTypeScheme
from app.tutorial.exceptions import TutorialExceptions
from app.tutorial.models import Tutorial
from app.tutorial.responses import TutorialResponses
from app.tutorial.schemas import AddTutorialScheme, EditTutorialScheme, GetDecodedTutorialScheme, TutorialIDScheme
from app.tutorial.theme.crud import get_theme
from app.tutorial.theme.schemas import GetTutorialThemeScheme
from app.tutorial.type.crud import get_tutorial_type
from app.tutorial.type.schemas import GetTutorialTypeScheme
from app.user.crud import get_user
from app.user.schemas import GetUserScheme


TutorID = Annotated[int, TutorialIDScheme]


@db_checker()
async def add_tutorial(tutor: AddTutorialScheme, db_session: AsyncSession) -> ResponseScheme:
    async with db_session as session:
        new_tutor = Tutorial(
            title=tutor.title,               # regexp
            type_code=tutor.type_code,
            theme_code=tutor.theme_code,
            description=tutor.description,   # regexp
            language_code=tutor.lang_code,
            source_link=str(tutor.source_link),
            dist_type_code=tutor.dist_type_code,
            who_added_id=tutor.who_added_id
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
                type=tutor_data.type_code,
                theme=tutor_data.theme_code,
                language=tutor_data.lang_code,
                description=tutor_data.description,    #regexp
                dist_type=tutor_data.dist_type_code,
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
        tutor: Tutorial | None = await session.get(Tutorial, tutor_id)
        if not tutor: raise TutorialExceptions.TUTORIAL_NOT_FOUND
        return AddTutorialScheme(
            title=tutor.title,
            type_code=tutor.type_code,
            theme_code=tutor.theme_code,
            description=tutor.description,
            lang_code=tutor.language_code,
            source_link=parse_obj_as(HttpUrl, tutor.source_link),
            dist_type_code=tutor.dist_type_code,
            who_added_id=tutor.who_added_id
        )


# All decoding operations will be on the client-side
@parameter_checker()
async def get_decoded_tutorial(tutor_id: TutorID, db_session: AsyncSession) -> GetDecodedTutorialScheme:
    tutor: AddTutorialScheme = await get_tutorial(tutor_id, db_session)

    decoded_type: GetTutorialTypeScheme = await get_tutorial_type(tutor.type_code, db_session)
    decoded_theme: GetTutorialThemeScheme = await get_theme(tutor.theme_code, db_session)
    decoded_lang: LanguageScheme = await get_language(tutor.lang_code, db_session)
    decoded_dist_type: GetTutorialDistTypeScheme = await get_distribution_type(tutor.dist_type_code, db_session)
    decoded_user: GetUserScheme = await get_user(tutor.who_added_id, db_session)

    return GetDecodedTutorialScheme(
        title=tutor.title,
        type=decoded_type.value,
        theme=decoded_theme.value,
        language=decoded_lang.value,
        description=tutor.description,
        dist_type=decoded_dist_type.dist_type_value,
        source_link=parse_obj_as(HttpUrl, tutor.source_link),
        who_added=decoded_user.name,
    )
