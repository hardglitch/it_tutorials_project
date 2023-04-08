from dataclasses import dataclass
from enum import StrEnum
from typing import Literal


class Language(StrEnum):
    rus: str = "rus"
    eng: str = "eng"

@dataclass()
class Table:

    @dataclass()
    class User:
        table_name: str = "user"
        id: str = "id"
        tutorial: str = "tutorial"

    @dataclass()
    class Tutorial:
        table_name: str = "tutorial"
        who_added: str = "who_added"
        language: Literal[Language.eng, Language.rus] = Language.rus
