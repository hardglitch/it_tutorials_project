from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.dictionary.schemas import DictionaryScheme
from src.language.crud import add_language
from src.language.schemas import LanguageScheme
from src.tutorial.dist_type.crud import add_distribution_type

ENGLISH: int


async def insert_languages(async_session: AsyncSession = Depends(get_session)):
    global ENGLISH
    ENGLISH = await add_language(LanguageScheme(abbreviation="eng", value="english", is_ui_lang=True), async_session)


async def insert_distribution_types(async_session: AsyncSession = Depends(get_session)):
    await add_distribution_type(DictionaryScheme(lang_code=5, value="free"), async_session)
    await add_distribution_type(DictionaryScheme(lang_code=5, value="unfree"), async_session)


async def insert_tutorial_themes():
    pass


async def insert_tutorial_types():
    pass


async def insert_users():
    pass

