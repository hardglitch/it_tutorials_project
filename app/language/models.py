from sqlalchemy import Boolean, Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.common.constants import Table
from app.db import Base


class Language(Base):
    __tablename__ = Table.Language.table_name
    code: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True, index=True)
    abbreviation: Mapped[str] = mapped_column(String(length=3), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    is_ui_lang: Mapped[bool] = mapped_column(Boolean, default=False)
