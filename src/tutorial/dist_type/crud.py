from typing import Annotated
from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.tutorial.dist_type.models import TutorialDistributionType
from src.tutorial.dist_type.schemas import TutorialDistributionTypeScheme


async def add_distribution_type(
        dist_type: TutorialDistributionTypeScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not dist_type or not async_session or \
       not all([param is not None for param in dist_type]): return False

    async with async_session as session:
        try:
            new_dist_type = TutorialDistributionType(
                code=dist_type.code,
                word_code=dist_type.word_code
            )
            session.add(new_dist_type)
            await session.commit()
            await session.refresh(new_dist_type)
            return True

        except Exception:
            raise


async def edit_distribution_type(
        dist_type: TutorialDistributionTypeScheme,
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not dist_type or not async_session or not all([param is not None for param in dist_type]): return False

    async with async_session as session:
        try:
            dist_type_from_db = await session.get(TutorialDistributionType, dist_type.code)
            dist_type_from_db.word_code = dist_type.word_code
            session.add(dist_type_from_db)
            await session.commit()
            await session.refresh(dist_type_from_db)
            return True

        except Exception:
            raise


async def delete_distribution_type(
        code: Annotated[int, Path(title="A Code of a Distribution Type")],
        async_session: AsyncSession = Depends(get_session)
) -> bool | None:

    if not code or not async_session: return False

    async with async_session as session:
        try:
            dist_type_from_db = await session.get(TutorialDistributionType, code)
            await session.delete(dist_type_from_db)
            await session.commit()
            return True

        except Exception:
            raise
