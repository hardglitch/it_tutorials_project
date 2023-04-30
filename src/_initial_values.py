from typing import Annotated, List
from fastapi import Body, Path
from pydantic import EmailStr, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.constants import Credential
from src.dictionary.schemas import AddWordToDictionaryScheme
from src.language.crud import add_language, get_all_languages
from src.language.schemas import EditLanguageScheme, LanguageScheme
from src.tutorial.crud import add_tutorial
from src.tutorial.dist_type.crud import add_distribution_type, get_all_distribution_types
from src.tutorial.dist_type.schemas import GetTutorialDistributionTypeScheme
from src.tutorial.schemas import AddTutorialScheme
from src.tutorial.theme.crud import add_theme, get_all_themes
from src.tutorial.theme.schemas import AddTutorialThemeScheme, GetTutorialThemeScheme
from src.tutorial.type.crud import add_tutorial_type, get_all_tutorial_types
from src.tutorial.type.schemas import GetTutorialTypeScheme
from src.user.crud import add_user, get_all_users
from src.user.schemas import AddUserScheme, GetUserScheme


async def insert_data(db_session: AsyncSession):

    # 1. Languages
    await add_language(LanguageScheme(abbreviation="eng", value="english", is_ui_lang=True), db_session)
    langs: List[EditLanguageScheme] = await get_all_languages(db_session)
    eng = langs[0]

    # 2. Distribution Types
    await add_distribution_type(AddWordToDictionaryScheme(lang_code=eng.lang_code, value="free"), db_session)
    await add_distribution_type(AddWordToDictionaryScheme(lang_code=eng.lang_code, value="unfree"), db_session)
    dist_types: List[GetTutorialDistributionTypeScheme] = await get_all_distribution_types(db_session)
    free = dist_types[0]
    unfree = dist_types[1]

    # 3. Tutorial Types
    await add_tutorial_type(AddWordToDictionaryScheme(lang_code=eng.lang_code, value="Programming"), db_session)
    await add_tutorial_type(AddWordToDictionaryScheme(lang_code=eng.lang_code, value="3D"), db_session)
    tutor_types: List[GetTutorialTypeScheme] = await get_all_tutorial_types(db_session)
    ddd = tutor_types[0]
    programming = tutor_types[1]

    # 4. Tutorial Themes
    await add_theme(AddTutorialThemeScheme(lang_code=eng.lang_code, value="Python", type_code=programming.type_code), db_session)
    await add_theme(AddTutorialThemeScheme(lang_code=eng.lang_code, value="Go", type_code=programming.type_code), db_session)
    await add_theme(AddTutorialThemeScheme(lang_code=eng.lang_code, value="Blender", type_code=ddd.type_code), db_session)
    tutor_themes: List[GetTutorialThemeScheme] = await get_all_themes(db_session)
    blender = tutor_themes[0]
    go = tutor_themes[1]
    python = tutor_themes[2]

    # 5. Users
    await add_user(
        AddUserScheme(name="Paul", credential=Credential.user, email=EmailStr("paul@email.com"), password="0987654321"),
        db_session
    )
    await add_user(
        AddUserScheme(name="John", credential=Credential.admin, email=EmailStr("john@email.com"), password="1234567890"),
        db_session
    )
    users: List[GetUserScheme] = await get_all_users(db_session)
    paul = users[0]
    john = users[1]

    # 6. Tutorials
    await add_tutorial(
        AddTutorialScheme(
            title="Python for beginners (2022)",
            type=programming.type_code,
            theme=python.theme_code,
            language=eng.lang_code,
            description="Super duper tutorial for all! It's really the best!",
            dist_type=free.dist_type_code,
            source_link="https://superdupertutorial.my",   # Just ignore the type mismatch error
            who_added=paul.id,
        ),
        db_session
    )
    await add_tutorial(
        AddTutorialScheme(
            title="Blender for Pro (2023)",
            type=ddd.type_code,
            theme=blender.theme_code,
            language=eng.lang_code,
            description="Super duper tutorial for all! It's really the best! Blender",
            dist_type=unfree.dist_type_code,
            source_link="https://blendertutor.com",      # Just ignore the type mismatch error
            who_added=john.id,
        ),
        db_session
    )
    await add_tutorial(
        AddTutorialScheme(
            title="Go Pro (2023)",
            type=programming.type_code,
            theme=go.theme_code,
            language=eng.lang_code,
            description="Programming on Go",
            dist_type=unfree.dist_type_code,
            source_link="https://goprog.go",             # Just ignore the type mismatch error
            who_added=john.id,
        ),
        db_session
    )
