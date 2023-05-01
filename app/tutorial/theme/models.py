from sqlalchemy import ForeignKey, Identity, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.common.constants import Table
from app.db import Base


class TutorialTheme(Base):
    __tablename__ = Table.Theme.table_name
    code: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True, index=True)
    word_code: Mapped[int] = mapped_column(Integer, nullable=False)
    type_code: Mapped[int] = mapped_column(Integer, ForeignKey(Table.Type.type_code))
