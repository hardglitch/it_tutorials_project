from dataclasses import dataclass
from enum import IntEnum
from typing import Dict


UI_LANGUAGE: int = 0
LANGUAGES: Dict[int, str] = {}          # {0: 'english'}   from DB
TUTORIAL_TYPES: Dict[int, str] = {}     # {0: 'Programming'}   from DB
TUTORIAL_THEMES: Dict[int, str] = {}    # {0: 'Some very important theme'}   from DB


class UILanguage(IntEnum):
    # Default values. They need to be retrieved from the database.
    eng = 0
    rus = 1
    ukr = 2


class LanguageAbbreviation(IntEnum):
    pass


class Credential(IntEnum):
    user: int = 0
    moderator: int = 1
    admin: int = 2


class ShareType(IntEnum):
    free: int = 0
    unfree: int = 1


@dataclass
class Table:

    @dataclass
    class User:
        table_name: str = "user"
        id: str = "id"
        user_id: str = table_name + "." + id
        tutorial: str = "tutorial"

    @dataclass
    class Tutorial:
        table_name: str = "tutorial"
        who_added: str = "who_added"

    @dataclass
    class Language:
        table_name: str = "language"
        id: str = "id"

    @dataclass
    class Theme:
        table_name: str = "theme"

    @dataclass
    class Type:
        table_name: str = "type"


@dataclass
class AccessToken:
    name: str = "access_token_to_it_tutorial_project"
    algorithm: str = "HS256"
    subject: str = "sub"
    user_id: str = "uid"
    expired: str = "exp"
    expiration_time: int = 15  # minutes
