from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, Path
from starlette import status
from starlette.responses import RedirectResponse, Response
from ...db import DBSession
from ...dictionary.schemas import DictWordCode, DictionarySchema, ValidDictValue
from ...language.schemas import LangCode
from ...tools import parameter_checker
from ...tutorial.dist_type.crud import add_dist_type, delete_dist_type, edit_dist_type, get_all_dist_types, \
    get_dist_type
from ...tutorial.dist_type.schemas import DistTypeCode, DistTypeSchema
from ...user.auth import is_admin


dist_type_router = APIRouter(prefix="/dt", tags=["Tutorial Distribution Type"])


@dist_type_router.post("/{ui_lang_code}/add", dependencies=[Depends(is_admin)])
@parameter_checker()
async def add_distribution_type(
        lang_code: Annotated[LangCode, Form()],
        dist_type_value: Annotated[ValidDictValue, Form()],
        db_session: DBSession,
        ui_lang_code: Annotated[LangCode, Path()],
        word_code: DictWordCode | None = Form(default=None),
) -> Response:

    if await add_dist_type(
        DictionarySchema(
            word_code=word_code,
            lang_code=lang_code,
            dict_value=dist_type_value,
        ),
        db_session=db_session
    ):
        return RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_302_FOUND)


@dist_type_router.post("/{ui_lang_code}/{dist_type_code}/edit", dependencies=[Depends(is_admin)])
@parameter_checker()
async def edit_distribution_type(
        dist_type_code: Annotated[DistTypeCode, Path()],
        lang_code: Annotated[LangCode, Form()],
        dist_type_value: Annotated[ValidDictValue, Form()],
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
) -> Response:

    if await edit_dist_type(
        DistTypeSchema(
            dist_type_code=dist_type_code,
            lang_code=lang_code,
            dict_value=dist_type_value,
        ),
        db_session=db_session
    ):
        return RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_302_FOUND)


@dist_type_router.post("/{ui_lang_code}/{dist_type_code}/del", dependencies=[Depends(is_admin)])
@parameter_checker()
async def delete_distribution_type(
        dist_type_code: Annotated[DistTypeCode, Path()],
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
) -> Response:

    if await delete_dist_type(
        dist_type_code=dist_type_code,
        db_session=db_session
    ):
        return RedirectResponse(url=f"/adm/{ui_lang_code}", status_code=status.HTTP_302_FOUND)


@dist_type_router.get("/{ui_lang_code}/{dist_type_code}", response_model_exclude_none=True)
@parameter_checker()
async def get_distribution_type(
        dist_type_code: Annotated[DistTypeCode, Path()],
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
) -> DistTypeSchema:

    return await get_dist_type(
        dist_type_code=dist_type_code,
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )


@dist_type_router.get("/{ui_lang_code}", response_model_exclude_none=True)
@parameter_checker()
async def get_all_distribution_types(
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
) -> List[DistTypeSchema]:

    return await get_all_dist_types(
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )
