from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, Path
from ...common.responses import ResponseSchema
from ...db import DBSession
from ...dictionary.schemas import DictWordCode, ValidDictValue
from ...language.schemas import LangCode
from ...tools import parameter_checker
from ...tutorial.theme.crud import add_theme, delete_theme, edit_theme, get_all_themes, get_theme
from ...tutorial.theme.schemas import ThemeSchema, ThemeCode
from ...tutorial.type.schemas import TypeCode
from ...user.auth import is_admin


theme_router = APIRouter(prefix="/theme", tags=["tutorial theme"])


@theme_router.post("/add", dependencies=[Depends(is_admin)])
@parameter_checker()
async def add__theme(
        lang_code: Annotated[LangCode, Form()],
        dict_value: Annotated[ValidDictValue, Form()],
        type_code: Annotated[TypeCode, Form()],
        db_session: DBSession,
        word_code: DictWordCode | None = Form(None),
) -> ResponseSchema:

    return await add_theme(
        ThemeSchema(
            word_code=word_code,
            lang_code=lang_code,
            dict_value=dict_value,
            type_code=type_code,
        ),
        db_session=db_session
    )


@theme_router.post("/{theme_code}/edit", dependencies=[Depends(is_admin)])
@parameter_checker()
async def edit__theme(
        theme_code: Annotated[ThemeCode, Path()],
        lang_code: Annotated[LangCode, Form()],
        dict_value: Annotated[ValidDictValue, Form()],
        type_code: Annotated[TypeCode, Form()],
        db_session: DBSession,
) -> ResponseSchema:

    return await edit_theme(
        ThemeSchema(
            theme_code=theme_code,
            lang_code=lang_code,
            dict_value=dict_value,
            type_code=type_code,
        ),
        db_session=db_session
    )


@theme_router.post("/{theme_code}/del", dependencies=[Depends(is_admin)])
@parameter_checker()
async def delete__theme(
        theme_code: Annotated[ThemeCode, Path()],
        db_session: DBSession,
) -> ResponseSchema:

    return await delete_theme(
        theme_code=theme_code,
        db_session=db_session
    )


@theme_router.get("/{theme_code}/{ui_lang_code}", response_model_exclude_none=True)
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


@theme_router.get("/", response_model_exclude_none=True)
@parameter_checker()
async def get__all_themes(
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession
) -> List[ThemeSchema]:

    return await get_all_themes(
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )
