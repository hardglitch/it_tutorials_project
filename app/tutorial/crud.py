from typing import List
from fastapi_cache.decorator import cache
from pydantic import HttpUrl, parse_obj_as
from sqlalchemy import ScalarResult, select, update
from ..common.responses import CommonResponses, ResponseSchema
from ..db import DBSession
from ..language.crud import get_lang
from ..language.schemas import LangCode, LanguageSchema
from ..tools import db_checker
from ..tutorial.dist_type.crud import get_dist_type
from ..tutorial.dist_type.schemas import DistTypeCode, DistTypeSchema
from ..tutorial.exceptions import TutorialExceptions
from ..tutorial.models import TutorialModel
from ..tutorial.schemas import DecodedTutorialSchema, TutorialID, TutorialSchema
from ..tutorial.theme.crud import get_theme
from ..tutorial.theme.schemas import ThemeCode, ThemeSchema
from ..tutorial.type.crud import get_type
from ..tutorial.type.schemas import TypeCode, TypeSchema
from ..user.crud import get_user
from ..user.schemas import UserSchema


@db_checker()
async def add_tutorial(tutor: TutorialSchema, db_session: DBSession) -> TutorialID:
    new_tutor = TutorialModel(
        title=tutor.title,
        type_code=tutor.type_code,
        theme_code=tutor.theme_code,
        description=tutor.description,
        language_code=tutor.lang_code,
        source_link=str(tutor.source_link),
        dist_type_code=tutor.dist_type_code,
        who_added_id=tutor.who_added_id
    )
    db_session.add(new_tutor)
    await db_session.commit()
    await db_session.refresh(new_tutor)
    return new_tutor.id


@db_checker()
async def edit_tutorial(tutor: TutorialSchema, db_session: DBSession) -> ResponseSchema:
    await db_session.execute(
        update(TutorialModel)
        .where(TutorialModel.id == tutor.id)
        .values(
            title=tutor.title,
            type=tutor.type_code,
            theme=tutor.theme_code,
            language=tutor.lang_code,
            description=tutor.description,
            dist_type=tutor.dist_type_code,
            source_link=tutor.source_link
        )
    )
    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def delete_tutorial(tutor_id: TutorialID, db_session: DBSession) -> ResponseSchema:
    await db_session.delete(
        select(TutorialModel)
        .where(TutorialModel.id == tutor_id)
    )
    await db_session.commit()
    return CommonResponses.SUCCESS


@db_checker()
async def get_tutorial(
        tutor_id: TutorialID,
        ui_lang_code: LangCode,
        db_session: DBSession
) -> DecodedTutorialSchema:

    tutor: TutorialSchema | None = await db_session.get(TutorialModel, tutor_id)
    if not tutor: raise TutorialExceptions.TUTORIAL_NOT_FOUND

    decoded_lang: LanguageSchema = await get_lang(
        lang_code=tutor.lang_code,
        db_session=db_session
    )
    decoded_user: UserSchema = await get_user(
        user_id=tutor.who_added_id,
        db_session=db_session
    )
    decoded_type: TypeSchema = await get_type(
        type_code=tutor.type_code,
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )
    decoded_theme: ThemeSchema = await get_theme(
        theme_code=tutor.theme_code,
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )
    decoded_dist_type: DistTypeSchema = await get_dist_type(
        dist_type_code=tutor.dist_type_code,
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )

    return DecodedTutorialSchema(
        id=tutor.id,
        title=tutor.title,
        type_code=tutor.type_code,
        type=decoded_type.dict_value,
        theme_code=tutor.theme_code,
        theme=decoded_theme.dict_value,
        lang_code=tutor.lang_code,
        language=decoded_lang.lang_value,
        description=tutor.description,
        dist_type_code=tutor.dist_type_code,
        dist_type=decoded_dist_type.dict_value,
        source_link=parse_obj_as(HttpUrl, tutor.source_link),
        who_added_id=tutor.who_added_id,
        who_added=decoded_user.name,
    )


@db_checker()
@cache(expire=300)
async def get_all_tutorials(
        ui_lang_code: LangCode,
        db_session: DBSession,
        type_code: TypeCode | None = None,
        theme_code: ThemeCode | None = None,
        dist_type_code: DistTypeCode | None = None,
        tutor_lang_code: LangCode | None = None,
) -> List[DecodedTutorialSchema]:

    if type_code:
        result: ScalarResult = await db_session.scalars(
            select(TutorialModel)
            .where(TutorialModel.type_code == type_code)
        )
    elif theme_code:
        result: ScalarResult = await db_session.scalars(
            select(TutorialModel)
            .where(TutorialModel.theme_code == theme_code)
        )
    elif dist_type_code:
        result: ScalarResult = await db_session.scalars(
            select(TutorialModel)
            .where(TutorialModel.dist_type_code == dist_type_code)
        )
    elif tutor_lang_code:
        result: ScalarResult = await db_session.scalars(
            select(TutorialModel)
            .where(TutorialModel.language_code == tutor_lang_code)
        )
    else:
        result: ScalarResult = await db_session.scalars(select(TutorialModel))

    tutors_list: List[DecodedTutorialSchema] = []

    for tutor in result:
        decoded_lang: LanguageSchema = await get_lang(
            lang_code=tutor.language_code,
            db_session=db_session
        )
        decoded_user: UserSchema = await get_user(
            user_id=tutor.who_added_id,
            db_session=db_session
        )
        decoded_type: TypeSchema = await get_type(
            type_code=tutor.type_code,
            ui_lang_code=ui_lang_code,
            db_session=db_session
        )
        decoded_theme: ThemeSchema = await get_theme(
            theme_code=tutor.theme_code,
            ui_lang_code=ui_lang_code,
            db_session=db_session
        )
        decoded_dist_type: DistTypeSchema = await get_dist_type(
            dist_type_code=tutor.dist_type_code,
            ui_lang_code=ui_lang_code,
            db_session=db_session
        )

        tutors_list.append(
            DecodedTutorialSchema(
                id=tutor.id,
                title=tutor.title,
                type_code=tutor.type_code,
                type=decoded_type.dict_value,
                theme_code=tutor.theme_code,
                theme=decoded_theme.dict_value,
                lang_code=tutor.language_code,
                language=decoded_lang.lang_value,
                description=tutor.description,
                dist_type_code=tutor.dist_type_code,
                dist_type=decoded_dist_type.dict_value,
                source_link=parse_obj_as(HttpUrl, tutor.source_link),
                who_added_id=tutor.who_added_id,
                who_added=decoded_user.name,
            )
        )
    return tutors_list
