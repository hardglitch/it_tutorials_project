from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.constants.constants import Table
from src.db import Base


class TutorialType(Base):
    __tablename__ = Table.Type.table_name
    code: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True, autoincrement=False)
    word_code: Mapped[int] = mapped_column(Integer, ForeignKey(Table.Dictionary.dictionary_word_code))
