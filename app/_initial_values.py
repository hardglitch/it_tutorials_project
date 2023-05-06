from typing import List
from pydantic import EmailStr, HttpUrl, SecretStr, parse_obj_as
from app.dictionary.schemas import DictionarySchema
from app.language.crud import add_lang, get_all_langs
from app.language.schemas import LanguageSchema
from app.tutorial.crud import add_tutorial
from app.tutorial.dist_type.crud import add_dist_type, get_all_dist_types
from app.tutorial.dist_type.schemas import DistTypeSchema
from app.tutorial.schemas import TutorialSchema
from app.tutorial.theme.crud import add_theme, get_all_themes
from app.tutorial.theme.schemas import ThemeSchema
from app.tutorial.type.crud import add_type, get_all_types
from app.tutorial.type.schemas import TypeSchema
from app.user.auth import Credential
from app.user.crud import add_user, get_all_users
from app.user.schemas import UserSchema


#  Just for testing

async def insert_data(db_session) -> None:

    # 1. Languages
    await add_lang(LanguageSchema(abbreviation="eng", lang_value="english", is_ui_lang=True), db_session=db_session)
    await add_lang(LanguageSchema(abbreviation="rus", lang_value="русский", is_ui_lang=True), db_session=db_session)
    langs: List[LanguageSchema] = await get_all_langs(db_session=db_session)
    eng = langs[0]
    rus = langs[1]

    # 2. Distribution Types
    await add_dist_type(DictionarySchema(lang_code=eng.lang_code, dict_value="free"), db_session=db_session)
    await add_dist_type(DictionarySchema(lang_code=eng.lang_code, dict_value="unfree"), db_session=db_session)
    await add_dist_type(DictionarySchema(lang_code=rus.lang_code, dict_value="бесплатно"), db_session=db_session)
    await add_dist_type(DictionarySchema(lang_code=rus.lang_code, dict_value="за деньги"), db_session=db_session)
    dist_types: List[DistTypeSchema] = await get_all_dist_types(ui_lang_code=rus.lang_code, db_session=db_session)
    free = dist_types[0]
    unfree = dist_types[1]

    # 3. Tutorial Types
    await add_type(DictionarySchema(lang_code=eng.lang_code, dict_value="Programming"), db_session=db_session)
    await add_type(DictionarySchema(lang_code=eng.lang_code, dict_value="3D"), db_session=db_session)
    await add_type(DictionarySchema(lang_code=rus.lang_code, dict_value="Программирование"), db_session=db_session)
    await add_type(DictionarySchema(lang_code=rus.lang_code, dict_value="3D"), db_session=db_session)
    tutor_types_eng: List[TypeSchema] = await get_all_types(ui_lang_code=eng.lang_code, db_session=db_session)
    tutor_types_rus: List[TypeSchema] = await get_all_types(ui_lang_code=rus.lang_code, db_session=db_session)
    ddd_eng = tutor_types_eng[0]
    programming_eng = tutor_types_eng[1]
    ddd_rus = tutor_types_rus[0]
    programming_rus = tutor_types_rus[1]

    # 4. Tutorial Themes
    await add_theme(ThemeSchema(lang_code=eng.lang_code, dict_value="Python", type_code=programming_eng.type_code))
    await add_theme(ThemeSchema(lang_code=eng.lang_code, dict_value="Go", type_code=programming_eng.type_code))
    await add_theme(ThemeSchema(lang_code=eng.lang_code, dict_value="Blender", type_code=ddd_eng.type_code))
    await add_theme(ThemeSchema(lang_code=rus.lang_code, dict_value="Python", type_code=programming_rus.type_code), db_session=db_session)
    await add_theme(ThemeSchema(lang_code=rus.lang_code, dict_value="Go", type_code=programming_rus.type_code), db_session=db_session)
    await add_theme(ThemeSchema(lang_code=rus.lang_code, dict_value="Blender", type_code=ddd_rus.type_code), db_session=db_session)
    tutor_themes: List[ThemeSchema] = await get_all_themes(ui_lang_code=eng.lang_code, db_session=db_session)
    blender_eng = tutor_themes[0]
    go_eng = tutor_themes[1]
    python_eng = tutor_themes[2]

    # 5. Users
    await add_user(
        UserSchema(name="Paul", credential=Credential.user, email=EmailStr("paul@email.com"), password=SecretStr(r"0987654321")),
        db_session=db_session
    )
    await add_user(
        UserSchema(name="John", credential=Credential.admin, email=EmailStr("john@email.com"), password=SecretStr("1234567890")),
        db_session=db_session
    )
    users: List[UserSchema] = await get_all_users(db_session=db_session)
    paul = users[0]
    john = users[1]

    # 6. Tutorials
    await add_tutorial(
        TutorialSchema(
            title="Python for beginners (2022)",
            type_code=programming_eng.type_code,
            theme_code=python_eng.theme_code,
            lang_code=eng.lang_code,
            description="Super duper tutorial for all! It's really the best!",
            dist_type_code=free.dist_type_code,
            source_link=parse_obj_as(HttpUrl, "https://superdupertutorial.my"),
            who_added_id=paul.id,
        ),
        db_session=db_session
    )
    await add_tutorial(
        TutorialSchema(
            title="Blender for Pro (2023)",
            type_code=ddd_eng.type_code,
            theme_code=blender_eng.theme_code,
            lang_code=eng.lang_code,
            description="Super duper tutorial for all! It's really the best! Blender",
            dist_type_code=unfree.dist_type_code,
            source_link=parse_obj_as(HttpUrl, "https://blendertutor.com"),
            who_added_id=john.id,
        ),
        db_session=db_session
    )
    await add_tutorial(
        TutorialSchema(
            title="Go Pro (2023)",
            type_code=programming_eng.type_code,
            theme_code=go_eng.theme_code,
            lang_code=eng.lang_code,
            description="Programming on Go",
            dist_type_code=unfree.dist_type_code,
            source_link=parse_obj_as(HttpUrl, "https://goprog.go"),
            who_added_id=john.id,
        ),
        db_session=db_session
    )
