from dataclasses import dataclass
from enum import IntEnum


class Credential(IntEnum):
    user: int = 0
    moderator: int = 1
    admin: int = 2


class Language(IntEnum):
    rus: int = 0
    eng: int = 1


class ShareType(IntEnum):
    free: int = 0
    unfree: int = 1


@dataclass
class Table:

    @dataclass
    class User:
        table_name: str = "user"
        id: str = table_name + ".id"
        tutorial: str = "tutorial"

    @dataclass
    class Tutorial:
        table_name: str = "tutorial"
        who_added: str = "who_added"
