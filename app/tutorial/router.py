from typing import Annotated, List
from fastapi import APIRouter, Depends, Form
from pydantic import HttpUrl
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response
from ..common.constants import PAGINATION_OFFSET, PageVars
from ..db import DBSession
from ..language.crud import UILangCode
from ..language.schemas import LangCode
from ..templates.render import render_template
from ..tools import parameter_checker
from ..tutorial.crud import add_tutorial, delete_tutorial, edit_tutorial, get_all_tutorials, get_tutorial, tutorial_page
from ..tutorial.dist_type.schemas import DistTypeCode
from ..tutorial.schemas import Pagination, TutorialID, TutorialListSchema, TutorialSchema, DecodedTutorialSchema, \
    ValidDescription, ValidTitle
from ..tutorial.theme.schemas import ThemeCode
from ..tutorial.type.schemas import TypeCode
from ..user.auth import decode_access_token, get_token, is_tutorial_editor


tutorial_router = APIRouter(prefix="/tt", tags=["Tutorial"])


@tutorial_router.get("/{ui_lang_code}/addp",
                     response_model_exclude_none=True, response_class=HTMLResponse, dependencies=[Depends(get_token)])
@parameter_checker()
async def add_tutorial_page(
        ui_lang_code: UILangCode,
        request: Request,
        db_session: DBSession,
) -> Response:

    return await tutorial_page(
        ui_lang_code=ui_lang_code,
        request=request,
        db_session=db_session,
    )


@tutorial_router.post("/{ui_lang_code}/add", response_model_exclude_none=True, dependencies=[Depends(get_token)])
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
        ui_lang_code: LangCode,
        db_session: DBSession,
) -> Response:

    if tutor_id := await add_tutorial(
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
    ):
        return RedirectResponse(url=f"/tt/{ui_lang_code}/{tutor_id}", status_code=status.HTTP_303_SEE_OTHER)


@tutorial_router.get("/{ui_lang_code}/{tutor_id}/editp", response_model_exclude_none=True)
@parameter_checker()
async def edit_tutorial_page(
        tutor_id: Annotated[TutorialID, Depends(is_tutorial_editor)],
        ui_lang_code: LangCode,
        request: Request,
        db_session: DBSession,
):
    return await tutorial_page(
        tutor_id=tutor_id,
        ui_lang_code=ui_lang_code,
        request=request,
        db_session=db_session,
    )


@tutorial_router.post("/{ui_lang_code}/{tutor_id}/edit", response_model_exclude_none=True)
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
        ui_lang_code: LangCode,
        db_session: DBSession,
) -> Response:

    if await edit_tutorial(
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
    ):
        return RedirectResponse(url=f"/tt/{ui_lang_code}/{tutor_id}", status_code=status.HTTP_303_SEE_OTHER)


@tutorial_router.post("/{ui_lang_code}/{tutor_id}/del")
@parameter_checker()
async def delete__tutorial(
        tutor_id: Annotated[TutorialID, Depends(is_tutorial_editor)],
        ui_lang_code: UILangCode,
        db_session: DBSession
) -> Response:

    if await delete_tutorial(
        tutor_id=tutor_id,
        db_session=db_session
    ):
        return RedirectResponse(url=f"/tt/{ui_lang_code}", status_code=status.HTTP_302_FOUND)


@tutorial_router.get("/{ui_lang_code}/{tutor_id}", response_class=HTMLResponse, response_model_exclude_none=True)
@parameter_checker()
async def get__tutorial(
        request: Request,
        db_session: DBSession,
        ui_lang_code: UILangCode,
        tutor_id: TutorialID,
) -> Response:

    tutor: DecodedTutorialSchema = \
        await get_tutorial(
            tutor_id=tutor_id,
            ui_lang_code=ui_lang_code,
            db_session=db_session,
        )

    is_editor: bool = True if await is_tutorial_editor(
        tutor_id=tutor_id,
        request=request,
        db_session=db_session,
        safe_mode=True
    ) else False

    page_vars = {
        PageVars.page: PageVars.Page.tutorial,
        PageVars.ui_lang_code: ui_lang_code,
        "editor": is_editor,
        "tutor": tutor,
    }
    return await render_template(
        request=request,
        db_session=db_session,
        page_vars=page_vars,
    )


@tutorial_router.get("/{ui_lang_code}", response_class=HTMLResponse, response_model_exclude_none=True)
@parameter_checker()
async def get__all_tutorials(
        request: Request,
        db_session: DBSession,
        ui_lang_code: UILangCode,
        page: Pagination = 1,
        type_code: TypeCode | None = None,
        theme_code: ThemeCode | None = None,
        dist_type_code: DistTypeCode | None = None,
        tutor_lang_code: LangCode | None = None,
) -> Response:

    tutors_list: TutorialListSchema = \
        await get_all_tutorials(
            ui_lang_code=ui_lang_code,
            type_code=type_code,
            theme_code=theme_code,
            dist_type_code=dist_type_code,
            tutor_lang_code=tutor_lang_code,
            page=page,
            db_session=db_session,
        )
    page_vars = {
        PageVars.page: PageVars.Page.main,
        PageVars.ui_lang_code: ui_lang_code,
        "tutors": tutors_list.tutorials,
        "current_page": page,
        "is_next_page": True if (tutors_list.total_count / PAGINATION_OFFSET) - page > 0 else False,
    }
    return await render_template(
        request=request,
        db_session=db_session,
        page_vars=page_vars,
    )
