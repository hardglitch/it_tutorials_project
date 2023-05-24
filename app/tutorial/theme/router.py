from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, Path
from starlette import status
from starlette.responses import RedirectResponse, Response

from ...common.responses import ResponseSchema
from ...db import DBSession
from ...dictionary.schemas import DictWordCode, ValidDictValue
from ...language.schemas import LangCode
from ...tools import parameter_checker
from ...tutorial.theme.crud import add_theme, delete_theme, edit_theme, get_all_themes, get_theme
from ...tutorial.theme.schemas import ThemeSchema, ThemeCode
from ...tutorial.type.schemas import TypeCode
from ...user.auth import is_admin


theme_router = APIRouter(prefix="", tags=["tutorial theme"])


@theme_router.post("/{ui_lang_code}/theme/add", dependencies=[Depends(is_admin)])
@parameter_checker()
async def add__theme(
        lang_code: Annotated[LangCode, Form()],
        theme_value: Annotated[ValidDictValue, Form()],
        type_code: Annotated[TypeCode, Form()],
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
        word_code: DictWordCode | None = Form(None),
) -> Response:

    if await add_theme(
        ThemeSchema(
            word_code=word_code,
            lang_code=lang_code,
            dict_value=theme_value,
            type_code=type_code,
        ),
        db_session=db_session
    ):
        return RedirectResponse(url=f"/{ui_lang_code}/admin", status_code=status.HTTP_302_FOUND)


@theme_router.post("/{ui_lang_code}/theme/{theme_code}/edit", dependencies=[Depends(is_admin)])
@parameter_checker()
async def edit__theme(
        theme_code: Annotated[ThemeCode, Path()],
        lang_code: Annotated[LangCode, Form()],
        theme_value: Annotated[ValidDictValue, Form()],
        type_code: Annotated[TypeCode, Form()],
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
) -> Response:

    if await edit_theme(
        ThemeSchema(
            theme_code=theme_code,
            lang_code=lang_code,
            dict_value=theme_value,
            type_code=type_code,
        ),
        db_session=db_session
    ):
        return RedirectResponse(url=f"/{ui_lang_code}/admin", status_code=status.HTTP_302_FOUND)


@theme_router.post("/{ui_lang_code}/theme/{theme_code}/del", dependencies=[Depends(is_admin)])
@parameter_checker()
async def delete__theme(
        theme_code: Annotated[ThemeCode, Path()],
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
) -> Response:

    if await delete_theme(
        theme_code=theme_code,
        db_session=db_session
    ):
        return RedirectResponse(url=f"/{ui_lang_code}/admin", status_code=status.HTTP_302_FOUND)


@theme_router.get("/{ui_lang_code}/theme/{theme_code}/", response_model_exclude_none=True)
@parameter_checker()
async def get__theme(
        theme_code: Annotated[ThemeCode, Path()],
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
) -> ThemeSchema:

    return await get_theme(
        theme_code=theme_code,
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )


@theme_router.get("/{ui_lang_code}/theme", response_model_exclude_none=True)
@parameter_checker()
async def get__all_themes(
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession
) -> List[ThemeSchema]:

    return await get_all_themes(
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )
