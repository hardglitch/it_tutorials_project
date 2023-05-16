from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, Path
from pydantic import HttpUrl
from starlette.requests import Request
from ..common.responses import ResponseSchema
from ..db import DBSession
from ..language.schemas import LangCode
from ..tools import parameter_checker
from ..tutorial.crud import add_tutorial, delete_tutorial, edit_tutorial, get_all_tutorials, get_tutorial
from ..tutorial.dist_type.router import dist_type_router
from ..tutorial.dist_type.schemas import DistTypeCode
from ..tutorial.schemas import TutorialID, TutorialSchema, DecodedTutorialSchema, ValidDescription, ValidTitle
from ..tutorial.theme.router import theme_router
from ..tutorial.theme.schemas import ThemeCode
from ..tutorial.type.router import type_router
from ..tutorial.type.schemas import TypeCode
from ..user.auth import decode_access_token, get_token, is_tutorial_editor


tutorial_router = APIRouter(prefix="/tutorial", tags=["tutorial"])
tutorial_router.include_router(dist_type_router)
tutorial_router.include_router(theme_router)
tutorial_router.include_router(type_router)


@tutorial_router.post("/add", dependencies=[Depends(get_token)])
@parameter_checker()
async def add__tutorial(
        title: Annotated[ValidTitle, Form()],
        description: Annotated[ValidDescription, Form()],
        link: Annotated[HttpUrl, Form()],
        type_code: Annotated[TypeCode, Form()],
        theme_code: Annotated[ThemeCode, Form()],
        lang_code: Annotated[LangCode, Form()],
        dist_type_code: Annotated[DistTypeCode, Form()],
        request: Request,
        db_session: DBSession,
) -> ResponseSchema:

    return await add_tutorial(
        TutorialSchema(
            title=title,
            description=description,
            source_link=link,
            type_code=type_code,
            theme_code=theme_code,
            lang_code=lang_code,
            dist_type_code=dist_type_code,
            who_added_id=decode_access_token(token=get_token(request)).id
        ),
        db_session=db_session
    )


@tutorial_router.put("/{tutor_id}/edit")
@parameter_checker()
async def edit__tutorial(
        tutor_id: Annotated[TutorialID, Depends(is_tutorial_editor)],
        title: Annotated[ValidTitle, Form()],
        description: Annotated[ValidDescription, Form()],
        link: Annotated[HttpUrl, Form()],
        type_code: Annotated[TypeCode, Form()],
        theme_code: Annotated[ThemeCode, Form()],
        lang_code: Annotated[LangCode, Form()],
        dist_type_code: Annotated[DistTypeCode, Form()],
        db_session: DBSession,
) -> ResponseSchema:

    return await edit_tutorial(
        TutorialSchema(
            id=tutor_id,
            title=title,
            description=description,
            source_link=link,
            type_code=type_code,
            theme_code=theme_code,
            lang_code=lang_code,
            dist_type_code=dist_type_code,
        ),
        db_session=db_session
    )


@tutorial_router.post("{tutor_id}/del")
@parameter_checker()
async def delete__tutorial(
        tutor_id: Annotated[TutorialID, Depends(is_tutorial_editor)],
        db_session: DBSession
) -> ResponseSchema:

    return await delete_tutorial(
        tutor_id=tutor_id,
        db_session=db_session
    )


@tutorial_router.get("/{tutor_id}", response_model_exclude_none=True)
@parameter_checker()
async def get__tutorial(
        tutor_id: Annotated[TutorialID, Path()],
        ui_lang_code: LangCode,
        db_session: DBSession,
) -> DecodedTutorialSchema:

    return await get_tutorial(
        tutor_id=tutor_id,
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )


@tutorial_router.get("/", response_model_exclude_none=True)
@parameter_checker()
async def get__all_tutorials(
        ui_lang_code: LangCode,
        db_session: DBSession,
        type_code: TypeCode | None = None,
        theme_code: ThemeCode | None = None,
) -> List[DecodedTutorialSchema]:

    return await get_all_tutorials(
        ui_lang_code=ui_lang_code,
        type_code=type_code,
        theme_code=theme_code,
        db_session=db_session
    )
