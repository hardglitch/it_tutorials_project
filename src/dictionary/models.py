from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.db import Base
from src.constants.constants import Table


class Dictionary(Base):
    __tablename__ = Table.Dictionary.table_name
    word_code: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True, autoincrement=False)
    eng: Mapped[str] = mapped_column(String(length=256), nullable=False)
    rus: Mapped[str] = mapped_column(String(length=256), nullable=False)
