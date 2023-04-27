from dataclasses import dataclass
from enum import IntEnum


class Credential(IntEnum):
    user: int = 0
    moderator: int = 1
    admin: int = 2


@dataclass
class Table:

    @dataclass
    class User:
        table_name: str = "user"
        id: str = "id"
        user_id: str = ".".join([table_name, id])
        added_tutorials: str = "added_tutorials"

    @dataclass
    class Tutorial:
        table_name: str = "tutorial"
        id: str = "id"
        tutorial_id: str = ".".join([table_name, id])

    @dataclass
    class Language:
        table_name: str = "language"
        code: str = "code"
        language_code: str = ".".join([table_name, code])

    @dataclass
    class Theme:
        table_name: str = "theme"
        code: str = "code"
        theme_code: str = ".".join([table_name, code])

    @dataclass
    class Type:
        table_name: str = "type"
        code: str = "code"
        type_code: str = ".".join([table_name, code])

    @dataclass
    class DistributionType:
        table_name: str = "distribution_type"
        code: str = "code"
        distribution_type_code: str = ".".join([table_name, code])

    @dataclass
    class Dictionary:
        table_name: str = "dictionary"
        word_code: str = "word_code"
        dictionary_word_code: str = ".".join([table_name, word_code])


@dataclass
class AccessToken:
    name: str = "access_token"
    algorithm: str = "HS256"
    subject: str = "sub"
    user_id: str = "uid"
    expired: str = "exp"
    expiration_time: int = 3600  # seconds
