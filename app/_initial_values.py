from typing import List
from pydantic import EmailStr, SecretStr
from .config import ADMIN_EMAIL, ADMIN_NAME, ADMIN_PASS
from .dictionary.schemas import DictionarySchema
from .language.crud import add_lang, get_all_langs
from .language.schemas import LanguageSchema
from .tutorial.dist_type.crud import add_dist_type, get_all_dist_types
from .tutorial.dist_type.schemas import DistTypeSchema
from .tutorial.theme.crud import add_theme, get_all_themes
from .tutorial.theme.schemas import ThemeSchema
from .tutorial.type.crud import add_type, get_all_types
from .tutorial.type.schemas import TypeSchema
from .user.crud import add_user
from .user.schemas import UserSchema


async def insert_default_data(db_session) -> None:

    # 1. Default Languages
    await add_lang(LanguageSchema(abbreviation="eng", lang_value="english", is_ui_lang=True), db_session=db_session)
    await add_lang(LanguageSchema(abbreviation="rus", lang_value="русский", is_ui_lang=True), db_session=db_session)
    await add_lang(LanguageSchema(abbreviation="ukr", lang_value="українська", is_ui_lang=True), db_session=db_session)
    langs: List[LanguageSchema] = await get_all_langs(db_session=db_session)
    eng = langs[0]
    rus = langs[1]
    ukr = langs[2]

    # 2. Distribution Types
    await add_dist_type(DictionarySchema(lang_code=eng.lang_code, dict_value="free"), db_session=db_session)
    dist_types_eng: List[DistTypeSchema] = await get_all_dist_types(ui_lang_code=eng.lang_code, db_session=db_session)
    free_eng = dist_types_eng[0]
    await add_dist_type(
        DictionarySchema(
            word_code=free_eng.word_code,
            lang_code=rus.lang_code,
            dict_value="бесплатно",
        ),
        db_session=db_session
    )
    await add_dist_type(
        DictionarySchema(
            word_code=free_eng.word_code,
            lang_code=ukr.lang_code,
            dict_value="безкоштовно",
        ),
        db_session=db_session
    )

    # 3. Tutorial Types
    await add_type(DictionarySchema(lang_code=eng.lang_code, dict_value="Programming"), db_session=db_session)
    types_eng: List[TypeSchema] = await get_all_types(ui_lang_code=eng.lang_code, db_session=db_session)
    prog_eng = types_eng[0]
    await add_type(
        DictionarySchema(
            word_code=prog_eng.word_code,
            lang_code=rus.lang_code,
            dict_value="Программирование",
        ),
        db_session=db_session
    )
    await add_type(
        DictionarySchema(
            word_code=prog_eng.word_code,
            lang_code=ukr.lang_code,
            dict_value="Програмування",
        ),
        db_session=db_session
    )

    # 4. Tutorial Themes
    await add_theme(
        ThemeSchema(
            lang_code=eng.lang_code,
            dict_value="Python",
            type_code=prog_eng.type_code
        ),
        db_session=db_session
    )
    themes_eng: List[ThemeSchema] = await get_all_themes(ui_lang_code=eng.lang_code, db_session=db_session)
    python_eng = themes_eng[0]
    await add_theme(
        ThemeSchema(
            type_code=prog_eng.type_code,
            word_code=python_eng.word_code,
            lang_code=rus.lang_code,
            dict_value="Python",
        ),
        db_session=db_session
    )
    await add_theme(
        ThemeSchema(
            type_code=prog_eng.type_code,
            word_code=python_eng.word_code,
            lang_code=ukr.lang_code,
            dict_value="Python",
        ),
        db_session=db_session
    )

    # 5. Admin
    await add_user(
        UserSchema(name=ADMIN_NAME, email=EmailStr(ADMIN_EMAIL), password=SecretStr(ADMIN_PASS)),
        db_session=db_session,
        is_admin=True
    )
