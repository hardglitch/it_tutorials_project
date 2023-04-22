from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.constants.constants import Table
from src.db import Base


class Language(Base):
    __tablename__ = Table.Language.table_name
    code: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True, autoincrement=False)
    abbreviation: Mapped[str] = mapped_column(String(length=3), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    is_ui_lang: Mapped[bool] = mapped_column(Boolean, default=False)
