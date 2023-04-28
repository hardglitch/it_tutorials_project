from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from src._initial_values_py import insert_languages, insert_distribution_types
from src.config import REDIS_HOST, REDIS_PASS, REDIS_PORT
from src.db import DBSession
from src.language.router import language_router
from src.tutorial.router import tutorial_router
from src.user.router import user_router
from redis import Redis, asyncio as aioredis


class MainRouter:
    def __init__(self, app: FastAPI):
        app.include_router(language_router)
        app.include_router(user_router)
        app.include_router(tutorial_router)

        @app.post("/_init_data", tags=["INIT"])
        async def _init_data(db_session: DBSession):
            # await insert_languages(async_session)
            await insert_distribution_types(db_session)
            pass

        @app.on_event("startup")
        async def startup():
            redis: Redis = aioredis.from_url(
                url=f"redis://{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0",
                encoding="utf-8",
                decode_responses=True
            )
            FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
