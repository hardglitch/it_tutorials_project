from fastapi import FastAPI
from src.user.router import user_router


class MainRouter:
    def __init__(self, app: FastAPI):
        app.include_router(user_router)

        # @app.get("/")
        # async def root():
        #     return {"message": "Hello World"}
        #
        # @app.get("/hello/{name}")
        # async def say_hello(name: str):
        #     return {"message": f"Hello {name}"}
