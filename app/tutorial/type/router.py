from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, Path
from starlette import status
from starlette.responses import RedirectResponse, Response
from ...db import DBSession
from ...dictionary.schemas import DictWordCode, DictionarySchema, ValidDictValue
from ...language.crud import UILangCode
from ...language.schemas import LangCode
from ...tools import parameter_checker
from ...tutorial.type.crud import add_type, delete_type, edit_type, get_all_types, get_type
from ...tutorial.type.schemas import TypeCode, TypeSchema
from ...user.auth import is_admin


type_router = APIRouter(prefix="/tp", tags=["Tutorial Type / Category"])


@type_router.post("/{ui_lang_code}/add", dependencies=[Depends(is_admin)])
@parameter_checker()
async def add_tutorial_type(
        lang_code: Annotated[LangCode, Form()],
        type_value: Annotated[ValidDictValue, Form()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
        word_code: DictWordCode | None = Form(default=None),
) -> Response:

    if await add_type(
        DictionarySchema(
            word_code=word_code,
            lang_code=lang_code,
            dict_value=type_value,
        ),
        db_session=db_session
    ):
        return RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_200_OK)


@type_router.post("/{ui_lang_code}/{type_code}/edit", dependencies=[Depends(is_admin)])
@parameter_checker()
async def edit_tutorial_type(
        type_code: Annotated[TypeCode, Path()],
        lang_code: Annotated[LangCode, Form()],
        type_value: Annotated[ValidDictValue, Form()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
):

    if await edit_type(
        TypeSchema(
            type_code=type_code,
            lang_code=lang_code,
            dict_value=type_value,
        ),
        db_session=db_session
    ):
        return RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_302_FOUND)


@type_router.post("/{ui_lang_code}/{type_code}/del", dependencies=[Depends(is_admin)])
@parameter_checker()
async def delete_tutorial_type(
        type_code: Annotated[TypeCode, Path()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
) -> Response:

    if await delete_type(
        type_code=type_code,
        db_session=db_session
    ):
        return RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_302_FOUND)


@type_router.get("/{ui_lang_code}/{type_code}", response_model_exclude_none=True)
@parameter_checker()
async def get_tutorial_type(
        type_code: Annotated[TypeCode, Path()],
        ui_lang_code: UILangCode,
        db_session: DBSession,
) -> TypeSchema:

    return await get_type(
        type_code=type_code,
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )


@type_router.get("/{ui_lang_code}", response_model_exclude_none=True)
@parameter_checker()
async def get_all_tutorial_types(
    ui_lang_code: UILangCode,
    db_session: DBSession,
) -> List[TypeSchema]:

    return await get_all_types(
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )
