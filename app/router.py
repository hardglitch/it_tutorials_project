from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from ._initial_values import insert_data
from .config import REDIS_HOST, REDIS_PASS, REDIS_PORT
from .db import DBSession
from .language.router import language_router
from .tutorial.router import tutorial_router
from .user.router import user_router
from redis import asyncio


class MainRouter:
    def __init__(self, app: FastAPI):

        origins = [
            "https://localhost:80",
            "https://localhost:8000",
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
        async def __init_data(db: DBSession) -> None:
            await insert_data(db)

        @app.on_event("startup")
        async def startup() -> None:
            redis = asyncio.from_url(
                url=f"redis://{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0",
                encoding="utf-8",
                decode_responses=True
            )
            FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
