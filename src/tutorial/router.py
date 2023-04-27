from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.db import get_session
from src.constants.constants import AccessToken
from src.tutorial.crud import create_tutorial, get_tutorial_from_db
from src.tutorial.dist_type.router import dist_type_router
from src.tutorial.models import Tutorial
from src.tutorial.schemas import DecryptedTutorialScheme, TutorialScheme
from src.tutorial.theme.router import theme_router
from src.tutorial.type.router import type_router
from src.user.auth import decode_access_token, oauth2_scheme
from src.constants.responses import UserResponses


tutorial_router = APIRouter(prefix="/tutorial", tags=["tutorial"])
tutorial_router.include_router(dist_type_router)
tutorial_router.include_router(theme_router)
tutorial_router.include_router(type_router)

