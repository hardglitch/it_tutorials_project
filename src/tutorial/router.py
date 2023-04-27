from fastapi import APIRouter
from src.tutorial.dist_type.router import dist_type_router
from src.tutorial.theme.router import theme_router
from src.tutorial.type.router import type_router


tutorial_router = APIRouter(prefix="/tutorial", tags=["tutorial"])
tutorial_router.include_router(dist_type_router)
tutorial_router.include_router(theme_router)
tutorial_router.include_router(type_router)
