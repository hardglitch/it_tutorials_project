from fastapi import FastAPI
from src.tutorial.router import tutorial_router
from src.user.router import user_router


class MainRouter:
    def __init__(self, app: FastAPI):
        app.include_router(user_router)
        app.include_router(tutorial_router)
