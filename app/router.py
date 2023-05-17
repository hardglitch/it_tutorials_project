import time
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.decorator import cache
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response
from ._initial_values import insert_data
from .common.constants import PageVars
from .common.exceptions import CommonExceptions
from .db import DBSession
from .language.crud import UILangCode
from .language.router import language_router
from .templates.render import render_template
from .tutorial.crud import get_all_tutorials
from .tutorial.router import tutorial_router
from .tutorial.schemas import DecodedTutorialSchema
from .tutorial.theme.schemas import ThemeCode
from .tutorial.type.schemas import TypeCode
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
            allow_methods=["POST", "GET", "PUT", "DELETE"],
            allow_headers=["*"],
        )

        app.include_router(language_router)
        app.include_router(user_router)
        app.include_router(tutorial_router)

        @app.get("/{ui_lang_code}", tags=["ROOT"], response_class=HTMLResponse)
        async def root(
            request: Request,
            db_session: DBSession,
            ui_lang_code: UILangCode,
            type_code: TypeCode | None = None,
            theme_code: ThemeCode | None = None,
        ):

            tutors_list: List[DecodedTutorialSchema] = \
                await get_all_tutorials(
                    ui_lang_code=ui_lang_code,
                    type_code=type_code,
                    theme_code=theme_code,
                    db_session=db_session
                )
            page_vars = {
                    PageVars.page: PageVars.Page.tutorials,
                    PageVars.ui_lang_code: ui_lang_code,
                    "tutors": tutors_list,
                }
            return await render_template(request=request, page_vars=page_vars)

        @app.get("/")
        async def redirect(ui_lang_code: UILangCode) -> Response:
            return RedirectResponse(url=f"/{ui_lang_code}", status_code=status.HTTP_302_FOUND)

        @app.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc: HTTPException):
            page_vars = {
                PageVars.page: PageVars.Page.exception,
                PageVars.code: exc.status_code,
                PageVars.detail: exc.detail
            }
            return await render_template(request=request, page_vars=page_vars)

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            page_vars = {
                PageVars.page: PageVars.Page.exception,
                PageVars.code: status.HTTP_400_BAD_REQUEST,
                PageVars.detail: CommonExceptions.INVALID_PARAMETERS.detail
            }
            return await render_template(request=request, page_vars=page_vars)

        @app.post("/init_data", tags=["TEST"])
        async def __init_data(db_session: DBSession) -> None:
            await insert_data(db_session)

        @app.get("/redis_test", tags=["TEST"])
        @cache()
        def redis_test():
            time.sleep(2)
            return {"detail": "Well Done!"}
