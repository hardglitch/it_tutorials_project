from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.language.crud import add_language
from src.language.schemas import LanguageScheme


async def insert_languages(async_session: AsyncSession = Depends(get_session)):
    await add_language(LanguageScheme(code=0, abbreviation="eng", value="english", is_ui_lang=True), async_session)
    await add_language(LanguageScheme(code=1, abbreviation="rus", value="русский", is_ui_lang=True), async_session)


async def insert_share_types():
    pass


async def insert_tutorial_themes():
    pass


async def insert_tutorial_types():
    pass


async def insert_words_into_dictionary():
    pass


async def insert_users():
    pass

