from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
# from app._initial_values_py import insert_data
from app.config import REDIS_HOST, REDIS_PASS, REDIS_PORT
from app.db import DBSession
from app.language.router import language_router
from app.tutorial.router import tutorial_router
from app.user.router import user_router
from redis import asyncio


class MainRouter:
    def __init__(self, app: FastAPI):

        origins = [
            "http://localhost",
            "http://localhost:8000",
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
