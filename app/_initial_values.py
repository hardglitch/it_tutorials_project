from typing import List
from pydantic import EmailStr, HttpUrl, parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession
from app.dictionary.schemas import AddWordToDictionarySchema
from app.language.crud import add_language, get_all_languages
from app.language.schemas import EditLanguageSchema, LanguageSchema
from app.tutorial.crud import add_tutorial
from app.tutorial.dist_type.crud import add_distribution_type, get_all_distribution_types
from app.tutorial.dist_type.schemas import GetTutorialDistTypeSchema
from app.tutorial.schemas import AddTutorialSchema
from app.tutorial.theme.crud import add_theme, get_all_themes
from app.tutorial.theme.schemas import AddTutorialThemeSchema, GetTutorialThemeSchema
from app.tutorial.type.crud import add_tutorial_type, get_all_tutorial_types
from app.tutorial.type.schemas import GetTutorialTypeSchema
from app.user.auth import Credential
from app.user.crud import add_user, get_all_users
from app.user.schemas import AddUserSchema, GetUserSchema


async def insert_data(db_session: AsyncSession) -> None:

    # 1. Languages
    await add_language(LanguageSchema(abbreviation="eng", value="english", is_ui_lang=True), db_session)
    langs: List[EditLanguageSchema] = await get_all_languages(db_session)
    eng = langs[0]

    # 2. Distribution Types
    await add_distribution_type(AddWordToDictionarySchema(lang_code=eng.lang_code, value="free"), db_session)
    await add_distribution_type(AddWordToDictionarySchema(lang_code=eng.lang_code, value="unfree"), db_session)
    dist_types: List[GetTutorialDistTypeSchema] = await get_all_distribution_types(db_session)
    free = dist_types[0]
    unfree = dist_types[1]

    # 3. Tutorial Types
    await add_tutorial_type(AddWordToDictionarySchema(lang_code=eng.lang_code, value="Programming"), db_session)
    await add_tutorial_type(AddWordToDictionarySchema(lang_code=eng.lang_code, value="3D"), db_session)
    tutor_types: List[GetTutorialTypeSchema] = await get_all_tutorial_types(db_session)
    ddd = tutor_types[0]
    programming = tutor_types[1]

    # 4. Tutorial Themes
    await add_theme(AddTutorialThemeSchema(lang_code=eng.lang_code, value="Python", type_code=programming.type_code), db_session)
    await add_theme(AddTutorialThemeSchema(lang_code=eng.lang_code, value="Go", type_code=programming.type_code), db_session)
    await add_theme(AddTutorialThemeSchema(lang_code=eng.lang_code, value="Blender", type_code=ddd.type_code), db_session)
    tutor_themes: List[GetTutorialThemeSchema] = await get_all_themes(db_session)
    blender = tutor_themes[0]
    go = tutor_themes[1]
    python = tutor_themes[2]

    # 5. Users
    await add_user(
        AddUserSchema(name="Paul", credential=Credential.user, email=EmailStr("paul@email.com"), password="0987654321"),
        db_session
    )
    await add_user(
        AddUserSchema(name="John", credential=Credential.admin, email=EmailStr("john@email.com"), password="1234567890"),
        db_session
    )
    users: List[GetUserSchema] = await get_all_users(db_session)
    paul = users[0]
    john = users[1]

    # 6. Tutorials
    await add_tutorial(
        AddTutorialSchema(
            title="Python for beginners (2022)",
            type_code=programming.type_code,
            theme_code=python.theme_code,
            lang_code=eng.lang_code,
            description="Super duper tutorial for all! It's really the best!",
            dist_type_code=free.dist_type_code,
            source_link=parse_obj_as(HttpUrl, "https://superdupertutorial.my"),
            who_added_id=paul.id,
        ),
        db_session
    )
    await add_tutorial(
        AddTutorialSchema(
            title="Blender for Pro (2023)",
            type_code=ddd.type_code,
            theme_code=blender.theme_code,
            lang_code=eng.lang_code,
            description="Super duper tutorial for all! It's really the best! Blender",
            dist_type_code=unfree.dist_type_code,
            source_link=parse_obj_as(HttpUrl, "https://blendertutor.com"),
            who_added_id=john.id,
        ),
        db_session
    )
    await add_tutorial(
        AddTutorialSchema(
            title="Go Pro (2023)",
            type_code=programming.type_code,
            theme_code=go.theme_code,
            lang_code=eng.lang_code,
            description="Programming on Go",
            dist_type_code=unfree.dist_type_code,
            source_link=parse_obj_as(HttpUrl, "https://goprog.go"),
            who_added_id=john.id,
        ),
        db_session
    )
