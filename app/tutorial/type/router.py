from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, Path
from ...common.responses import ResponseSchema
from ...db import DBSession
from ...dictionary.schemas import DictWordCode, DictionarySchema, ValidDictValue
from ...language.schemas import LangCode
from ...tools import parameter_checker
from ...tutorial.type.crud import add_type, delete_type, edit_type, get_all_types, get_type
from ...tutorial.type.schemas import TypeCode, TypeSchema
from ...user.auth import is_admin


type_router = APIRouter(prefix="/type", tags=["tutorial type"])


@type_router.post("/add", dependencies=[Depends(is_admin)])
@parameter_checker()
async def add_tutorial_type(
        lang_code: Annotated[LangCode, Form()],
        type_value: Annotated[ValidDictValue, Form()],
        db_session: DBSession,
        word_code: DictWordCode | None = Form(None),
) -> ResponseSchema:

    return await add_type(
        DictionarySchema(
            word_code=word_code,
            lang_code=lang_code,
            dict_value=type_value,
        ),
        db_session=db_session
    )


@type_router.post("/{type_code}/edit", dependencies=[Depends(is_admin)])
@parameter_checker()
async def edit_tutorial_type(
        type_code: Annotated[TypeCode, Path()],
        lang_code: Annotated[LangCode, Form()],
        type_value: Annotated[ValidDictValue, Form()],
        db_session: DBSession,
) -> ResponseSchema:

    return await edit_type(
        TypeSchema(
            type_code=type_code,
            lang_code=lang_code,
            dict_value=type_value,
        ),
        db_session=db_session
    )


@type_router.post("/{type_code}/del", dependencies=[Depends(is_admin)])
@parameter_checker()
async def delete_tutorial_type(
        type_code: Annotated[TypeCode, Path()],
        db_session: DBSession,
) -> ResponseSchema:

    return await delete_type(
        type_code=type_code,
        db_session=db_session
    )


@type_router.get("/get-all", response_model_exclude_none=True)
@parameter_checker()
async def get_all_tutorial_types(
    ui_lang_code: Annotated[LangCode, Path()],
    db_session: DBSession,
) -> List[TypeSchema]:

    return await get_all_types(
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )


@type_router.get("/{type_code}/{ui_lang_code}", response_model_exclude_none=True)
@parameter_checker()
async def get_tutorial_type(
        type_code: Annotated[TypeCode, Path()],
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
) -> TypeSchema:

    return await get_type(
        type_code=type_code,
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )
