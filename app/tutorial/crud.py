from typing import Annotated
from pydantic import HttpUrl, parse_obj_as
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import CommonExceptions
from app.common.responses import CommonResponses, ResponseSchema
from app.language.crud import get_language
from app.language.schemas import LanguageSchema
from app.tools import db_checker, parameter_checker
from app.tutorial.dist_type.crud import get_distribution_type
from app.tutorial.dist_type.schemas import GetTutorialDistTypeSchema
from app.tutorial.exceptions import TutorialExceptions
from app.tutorial.models import TutorialModel
from app.tutorial.responses import TutorialResponses
from app.tutorial.schemas import AddTutorialSchema, EditTutorialSchema, GetDecodedTutorialSchema, TutorialIDSchema
from app.tutorial.theme.crud import get_theme
from app.tutorial.theme.schemas import GetTutorialThemeSchema
from app.tutorial.type.crud import get_tutorial_type
from app.tutorial.type.schemas import GetTutorialTypeSchema
from app.user.crud import get_user
from app.user.schemas import UserSchema


TutorID = Annotated[int, TutorialIDSchema]


@db_checker()
async def add_tutorial(tutor: AddTutorialSchema, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        title = " ".join(tutor.title.split())
        description = " ".join(tutor.title.split())
        if not title or not description: raise CommonExceptions.INVALID_PARAMETERS

        new_tutor = TutorialModel(
            title=title,
            type_code=tutor.type_code,
            theme_code=tutor.theme_code,
            description=description,
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
async def edit_tutorial(tutor_id: TutorID, tutor_data: EditTutorialSchema, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        title = " ".join(tutor_data.title.split())
        description = " ".join(tutor_data.title.split())
        if not title or not description: raise CommonExceptions.INVALID_PARAMETERS

        await session.execute(
            update(TutorialModel)
            .where(TutorialModel.id == tutor_id)
            .values(
                title=title,
                type=tutor_data.type_code,
                theme=tutor_data.theme_code,
                language=tutor_data.lang_code,
                description=description,
                dist_type=tutor_data.dist_type_code,
                source_link=tutor_data.source_link
            )
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def delete_tutorial(tutor_id: TutorID, db_session: AsyncSession) -> ResponseSchema:
    async with db_session as session:
        await session.delete(
            select(TutorialModel)
            .where(TutorialModel.id == tutor_id)
        )
        await session.commit()
        return CommonResponses.SUCCESS


@db_checker()
async def get_tutorial(tutor_id: TutorID, db_session: AsyncSession) -> AddTutorialSchema:
    async with db_session as session:
        tutor: TutorialModel | None = await session.get(TutorialModel, tutor_id)
        if not tutor: raise TutorialExceptions.TUTORIAL_NOT_FOUND
        return AddTutorialSchema(
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
async def get_decoded_tutorial(tutor_id: TutorID, db_session: AsyncSession) -> GetDecodedTutorialSchema:
    tutor: AddTutorialSchema = await get_tutorial(tutor_id, db_session)

    decoded_type: GetTutorialTypeSchema = await get_tutorial_type(tutor.type_code, db_session)
    decoded_theme: GetTutorialThemeSchema = await get_theme(tutor.theme_code, db_session)
    decoded_lang: LanguageSchema = await get_language(tutor.lang_code, db_session)
    decoded_dist_type: GetTutorialDistTypeSchema = await get_distribution_type(tutor.dist_type_code, db_session)
    decoded_user: UserSchema = await get_user(tutor.who_added_id, db_session)

    return GetDecodedTutorialSchema(
        title=tutor.title,
        type=decoded_type.value,
        theme=decoded_theme.value,
        language=decoded_lang.value,
        description=tutor.description,
        dist_type=decoded_dist_type.dist_type_value,
        source_link=parse_obj_as(HttpUrl, tutor.source_link),
        who_added=decoded_user.name,
    )
