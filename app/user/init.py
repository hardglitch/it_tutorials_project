from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from app.common.constants import Credential
from app.tools import hard_clean_text


