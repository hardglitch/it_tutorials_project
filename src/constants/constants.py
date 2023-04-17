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
        id: str = "id"
        user_id: str = table_name + "." + id
        tutorial: str = "tutorial"

    @dataclass
    class Tutorial:
        table_name: str = "tutorial"
        who_added: str = "who_added"


@dataclass
class AccessToken:
    name: str = "access_token_to_it_tutorial_project"
    algorithm: str = "HS256"
    subject: str = "sub"
    user_id: str = "uid"
    expired: str = "exp"
    expiration_time: int = 15  # minutes
