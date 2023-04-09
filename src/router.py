from fastapi import FastAPI
from src.user.router import user_router


class MainRouter:
    def __init__(self, app: FastAPI):
        app.include_router(user_router)
