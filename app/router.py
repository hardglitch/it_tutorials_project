import time
from pathlib import Path
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.decorator import cache
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.staticfiles import StaticFiles
from ._initial_values import insert_data
from .admin import admin_router
from .common.constants import PageVars
from .common.exceptions import CommonExceptions
from .db import DBSession
from .language.crud import UILangCode
from .language.router import language_router
from .templates.render import render_template
from .tutorial.dist_type.router import dist_type_router
from .tutorial.router import tutorial_router
from .tutorial.theme.router import theme_router
from .tutorial.type.router import type_router
from .user.router import user_router


class MainRouter:
    def __init__(self, app: FastAPI):

        origins = [
            "https://localhost",
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["POST", "GET"],
            allow_headers=["*"],
        )

        app.include_router(admin_router)
        app.include_router(language_router)
        app.include_router(user_router)
        app.include_router(tutorial_router)
        app.include_router(dist_type_router)
        app.include_router(theme_router)
        app.include_router(type_router)

        app.mount("/static", StaticFiles(directory=Path(__name__.split(".")[0]).joinpath("static")), name="static")

        @app.get("/")
        async def redirect(ui_lang_code: UILangCode) -> Response:
            return RedirectResponse(url=f"/tt/{ui_lang_code}", status_code=status.HTTP_302_FOUND)

        @app.exception_handler(HTTPException)
        async def http_exception_handler(
                request: Request,
                exc: HTTPException,
        ):
            page_vars = {
                PageVars.page: PageVars.Page.exception,
                PageVars.code: exc.status_code,
                PageVars.detail: exc.detail,
            }
            return await render_template(
                request=request,
                page_vars=page_vars,
            )

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(
                request: Request,
                exc: RequestValidationError,
        ):
            page_vars = {
                PageVars.page: PageVars.Page.exception,
                PageVars.code: status.HTTP_400_BAD_REQUEST,
                PageVars.detail: CommonExceptions.INVALID_PARAMETERS.detail
            }
            return await render_template(
                request=request,
                page_vars=page_vars,
            )

        # ----------  TESTING -----------------------------

        @app.post("/init_data", tags=["TEST"])
        async def __init_data(db_session: DBSession) -> None:
            await insert_data(db_session)

        @app.get("/redis_test", tags=["TEST"])
        @cache()
        def redis_test():
            time.sleep(2)
            return {"detail": "Well Done!"}
