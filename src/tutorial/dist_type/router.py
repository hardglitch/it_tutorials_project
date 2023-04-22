from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.constants.constants import AccessToken
from src.constants.responses import CommonResponses, UserResponses
from src.db import get_session
from src.tutorial.dist_type.crud import add_distribution_type, edit_distribution_type
from src.tutorial.dist_type.schemas import TutorialDistributionTypeScheme
from src.user.auth import oauth2_scheme


dist_router = APIRouter(prefix="/dist_type", tags=["distribution_type"])


@dist_router.post("/add")
async def add_new_distribution_type(
        request: Request,
        dist_type: TutorialDistributionTypeScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if not token: return UserResponses.ACCESS_DENIED

    return CommonResponses.SUCCESS if await add_distribution_type(dist_type, async_session) \
        else CommonResponses.FAILED


@dist_router.patch("/edit")
async def edit_existing_distribution_type(
        request: Request,
        dist_type: TutorialDistributionTypeScheme,
        async_session: AsyncSession = Depends(get_session)
) -> str:

    if not dist_type: return CommonResponses.FAILED

    token: Annotated[str, Depends(oauth2_scheme)] = request.cookies.get(AccessToken.name)
    if not token: return UserResponses.ACCESS_DENIED

    return CommonResponses.SUCCESS if await edit_distribution_type(dist_type, async_session) \
        else CommonResponses.FAILED
