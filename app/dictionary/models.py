from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base
from app.common.constants import Table


class DictionaryModel(Base):
    __tablename__ = Table.Dictionary.table_name
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word_code: Mapped[int] = mapped_column(Integer, index=True, nullable=False, unique=False)
    lang_code: Mapped[int] = mapped_column(Integer, ForeignKey(Table.Language.language_code), unique=False)
    value: Mapped[str] = mapped_column(String(length=256), nullable=False)
