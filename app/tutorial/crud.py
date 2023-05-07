from pydantic import HttpUrl, parse_obj_as
from sqlalchemy import select, update
from ..common.responses import CommonResponses, ResponseSchema
from ..db import DBSession
from ..language.crud import get_lang
from ..language.schemas import LangCode, LanguageSchema
from ..tools import db_checker, parameter_checker
from ..tutorial.dist_type.crud import get_dist_type
from ..tutorial.dist_type.schemas import DistTypeSchema
from ..tutorial.exceptions import TutorialExceptions
from ..tutorial.models import TutorialModel
from ..tutorial.responses import TutorialResponses
from ..tutorial.schemas import DecodedTutorialSchema, TutorialID, TutorialSchema
from ..tutorial.theme.crud import get_theme
from ..tutorial.theme.schemas import ThemeSchema
from ..tutorial.type.crud import get_type
from ..tutorial.type.schemas import TypeSchema
from ..user.crud import get_user
from ..user.schemas import UserSchema


@db_checker()
async def add_tutorial(tutor: TutorialSchema, db_session: DBSession) -> ResponseSchema:
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
    return TutorialResponses.TUTORIAL_ADDED


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
async def get_tutorial(tutor_id: TutorialID, db_session: DBSession) -> TutorialSchema:
    tutor: TutorialModel | None = await db_session.get(TutorialModel, tutor_id)
    if not tutor: raise TutorialExceptions.TUTORIAL_NOT_FOUND
    return TutorialSchema(
        title=tutor.title,
        type_code=tutor.type_code,
        theme_code=tutor.theme_code,
        description=tutor.description,
        lang_code=tutor.language_code,
        source_link=parse_obj_as(HttpUrl, tutor.source_link),
        dist_type_code=tutor.dist_type_code,
        who_added_id=tutor.who_added_id
    )


@parameter_checker()
async def get_decoded_tutorial(
        tutor_id: TutorialID,
        ui_lang_code: LangCode,
        db_session: DBSession
) -> DecodedTutorialSchema:

    tutor: TutorialSchema = await get_tutorial(
        tutor_id=tutor_id,
        db_session=db_session
    )
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

    # result: Result = await db_session.execute(
    #     select(
    #         TutorialModel.title,
    #         TutorialModel.description,
    #         TutorialModel.source_link,
    #         LanguageModel.value,
    #         UserModel.name,
    #     )
    #     .where(and_(
    #         TutorialModel.id == tutor_id,
    #         LanguageModel.code == TutorialModel.language_code,
    #         UserModel.id == TutorialModel.who_added_id,
    #         DictionaryModel.lang_code == ui_lang_code,
    #     ))
    #     .distinct()
    # )
    # tutor: Row = result.one()

    return DecodedTutorialSchema(
        title=tutor.title,
        type=decoded_type.dict_value,
        theme=decoded_theme.dict_value,
        language=decoded_lang.lang_value,
        description=tutor.description,
        dist_type=decoded_dist_type.dict_value,
        source_link=parse_obj_as(HttpUrl, tutor.source_link),
        who_added=decoded_user.name,
    )
