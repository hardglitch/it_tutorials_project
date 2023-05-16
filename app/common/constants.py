from dataclasses import dataclass
from enum import IntEnum, StrEnum
from pathlib import Path
from starlette.templating import Jinja2Templates


templates_dir = Path(__name__.split(".")[0]).joinpath("templates")
templates = Jinja2Templates(directory=templates_dir)
# app.mount("/static", StaticFiles(directory=Path(__name__.split(".")[0]).joinpath("static")), name="static")

DEFAULT_UI_LANGUAGE: str = "eng"


class Credential(IntEnum):
    user = 1
    moderator = 2
    admin = 5


class DecodedCredential(StrEnum):
    user = Credential.user.name
    moderator = Credential.moderator.name
    admin = Credential.admin.name


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
    exp_delta: int = 3600  # seconds
