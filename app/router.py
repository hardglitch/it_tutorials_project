from pathlib import Path
from typing import List
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from ._initial_values import insert_data
from .config import REDIS_HOST, REDIS_PASS, REDIS_PORT
from .db import DBSession
from .language.crud import get_lang
from .language.router import language_router
from .language.schemas import LanguageSchema
from .tutorial.router import get__all_decoded_tutorials, get__decoded_tutorial, get__tutorial, tutorial_router
from .tutorial.schemas import DecodedTutorialSchema
from .user.router import user_router
from redis import asyncio


class MainRouter:
    def __init__(self, app: FastAPI, templates: Jinja2Templates):

        origins = [
            "https://localhost",
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["POST", "GET", "PUT", "DELETE"],
            allow_headers=["*"],
        )

        app.include_router(language_router)
        app.include_router(user_router)
        app.include_router(tutorial_router)

        # app.mount("/static", StaticFiles(directory="static"), name="static")

        @app.post("/init_data", tags=["INIT"])
        async def __init_data(db_session: DBSession) -> None:
            await insert_data(db_session)

        @app.on_event("startup")
        async def startup() -> None:
            redis = asyncio.from_url(
                url=f"redis://{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0",
                encoding="utf-8",
                decode_responses=True
            )
            FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

        @app.get("/", tags=["ROOT"], response_class=HTMLResponse)
        async def root(request: Request, db_session: DBSession):
            tutors_list: List[DecodedTutorialSchema] = \
                await get__all_decoded_tutorials(ui_lang_code=23, db_session=db_session)
            ui_lang: LanguageSchema = await get_lang(lang_code=23, db_session=db_session)
            return templates.TemplateResponse(
                name=f"tutorials.html",
                context={"request": request, "tutors": tutors_list, "ui_lang": ui_lang}
            )
