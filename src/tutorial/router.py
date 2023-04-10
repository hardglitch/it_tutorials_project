from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session

tutorial_router = APIRouter(prefix="/tutorial", tags=["tutorial"])


@tutorial_router.get("/{tutorial_id}")
async def get_tutorial(tutorial_id: int, async_session: AsyncSession = Depends(get_session)):
    pass