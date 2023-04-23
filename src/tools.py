import re
from typing import Dict
from sqlalchemy import Result, select
from src.db import get_session
from src.dictionary.models import Dictionary


async def _get_all_dictionary_values_by_language(lang: int = 0) -> Dict[str, str]:
    async with get_session() as session:
        result: Result = await session.execute(
            select(Dictionary.word_code, Dictionary.value).where(Dictionary.lang == lang)
        )
        res: Dict[str, str] = {}
        for row in result:
            key = _cleared_value(row.value) + "_" + row.word_code   # SomeValue_1
            res[key] = row.value
        return res  # {'SomeValue_1': 'Some value'}


def _cleared_value(value: str) -> str:
    return re.sub(r"[^a-zA-Z]", "", value.title())


def convert_values_to_attributes(values: Dict[str, str], obj: object):
    for value in values.items():
        setattr(obj, value[0], value[1])

