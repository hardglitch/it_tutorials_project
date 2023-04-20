from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from src.constants.constants import UI_LANGUAGE
from src.db import get_session
from src.language.crud import get_all_languages
from src.language.router import language_router
from src.tutorial.crud import get_all_tutorial_themes_by_ui_language, get_all_tutorial_types_by_ui_language
from src.tutorial.router import tutorial_router
from src.user.router import user_router


class MainRouter:
    def __init__(self, app: FastAPI):
        app.include_router(language_router)
        app.include_router(user_router)
        app.include_router(tutorial_router)

        # @app.on_event("startup")
        # async def startup_event(async_session: AsyncSession = Depends(get_session)):
        #     await get_all_languages(async_session)
        #     await get_all_tutorial_themes_by_ui_language(UI_LANGUAGE, async_session)
        #     await get_all_tutorial_types_by_ui_language(UI_LANGUAGE, async_session)
