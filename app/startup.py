from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio
from app.config import REDIS_HOST, REDIS_PASS, REDIS_PORT


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    redis = asyncio.from_url(
        url=f"redis://{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/0",
        encoding="utf-8",
        decode_responses=False
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await FastAPICache.clear()
