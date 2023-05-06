from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, Path
from app.common.responses import ResponseSchema
from app.db import DBSession
from app.dictionary.schemas import DictWordCode, DictionarySchema, ValidDictValue
from app.language.schemas import LangCode
from app.tools import parameter_checker
from app.tutorial.dist_type.crud import add_dist_type, delete_dist_type, edit_dist_type, get_all_dist_types, \
    get_dist_type
from app.tutorial.dist_type.schemas import DistTypeCode, DistTypeSchema
from app.user.auth import is_admin


dist_type_router = APIRouter(prefix="/dist-type", tags=["tutorial distribution type"])


@dist_type_router.post("/add", dependencies=[Depends(is_admin)])
@parameter_checker()
async def add_distribution_type(
        lang_code: Annotated[LangCode, Form()],
        dist_type_value: Annotated[ValidDictValue, Form()],
        db_session: DBSession,
        word_code: DictWordCode | None = Form(default=None),
) -> ResponseSchema:

    return await add_dist_type(
        DictionarySchema(
            word_code=word_code,
            lang_code=lang_code,
            dict_value=dist_type_value,
        ),
        db_session=db_session
    )


@dist_type_router.post("/{dist_type_code}/edit", dependencies=[Depends(is_admin)])
@parameter_checker()
async def edit_distribution_type(
        dist_type_code: Annotated[DistTypeCode, Path()],
        lang_code: Annotated[LangCode, Form()],
        dist_type_value: Annotated[ValidDictValue, Form()],
        db_session: DBSession,
) -> ResponseSchema:

    return await edit_dist_type(
        DistTypeSchema(
            dist_type_code=dist_type_code,
            lang_code=lang_code,
            dict_value=dist_type_value,
        ),
        db_session=db_session
    )


@dist_type_router.post("/{dist_type_code}/del", dependencies=[Depends(is_admin)])
@parameter_checker()
async def delete_distribution_type(
        dist_type_code: Annotated[DistTypeCode, Path()],
        db_session: DBSession,
) -> ResponseSchema:

    return await delete_dist_type(
        dist_type_code=dist_type_code,
        db_session=db_session
    )


@dist_type_router.get("/get-all/{ui_lang_code}", response_model_exclude_none=True)
@parameter_checker()
async def get_all_distribution_types(
        ui_lang_code: Annotated[LangCode, Path()],
        db_session: DBSession,
) -> List[DistTypeSchema]:

    return await get_all_dist_types(
        ui_lang_code=ui_lang_code,
        db_session=db_session
    )


@dist_type_router.get("/{dist_type_code}/{ui_lang_code}", response_model_exclude_none=True)
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

