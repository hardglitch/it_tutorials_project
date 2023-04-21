from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.constants import LANGUAGES
from src.db import get_session
from src.language.crud import get_all_languages


async def startup_ops():
    async_session: AsyncSession = Depends(get_session)
    await get_all_languages(async_session)
    print(LANGUAGES)
#     await get_all_tutorial_themes_by_ui_language(UI_LANGUAGE, async_session)
#     await get_all_tutorial_types_by_ui_language(UI_LANGUAGE, async_session)
