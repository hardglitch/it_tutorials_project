from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from ._initial_values import insert_data
from .db import DBSession
from .language.router import language_router
from .language.schemas import LangCode
from .tutorial.router import get__all_tutorials, tutorial_router
from .tutorial.schemas import DecodedTutorialSchema
from .tutorial.theme.schemas import ThemeCode
from .tutorial.type.schemas import TypeCode
from .user.auth import decode_access_token, get_token
from .user.router import user_router


class MainRouter:
    def __init__(self, app: FastAPI, templates: Jinja2Templates):

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

        # app.mount("/static", StaticFiles(directory="static"), name="static")

        @app.post("/init_data", tags=["INIT"])
        async def __init_data(db_session: DBSession) -> None:
            await insert_data(db_session)

        @app.get("/", tags=["ROOT"], response_class=HTMLResponse)
        async def root(
            request: Request,
            db_session: DBSession,
            ui_lang_code: LangCode | None = 23,
            type_code: TypeCode | None = None,
            theme_code: ThemeCode | None = None,
        ):

            tutors_list: List[DecodedTutorialSchema] = \
                await get__all_tutorials(
                    ui_lang_code=ui_lang_code,
                    type_code=type_code,
                    theme_code=theme_code,
                    db_session=db_session
                )

            # ui_lang: LanguageSchema = await get_lang(lang_code=23, db_session=db_session)
            token = get_token(request)
            auth: bool = False if token == "None" else True
            current_user_data = decode_access_token(token) if auth else ""

            return templates.TemplateResponse(
                name="tutorials.html",
                context={
                    "request": request,
                    "tutors": tutors_list,
                    "ui_lang_code": 23,
                    "auth": auth,
                    "current_user": current_user_data,
                }
            )

        @app.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc: HTTPException):
            return templates.TemplateResponse(
                name="exception.html",
                context={"request": request, "code": exc.status_code, "detail": exc.detail}
            )

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            return templates.TemplateResponse(
                name="exception.html",
                context={"request": request, "code": 400, "detail": "Invalid parameters"}
            )

