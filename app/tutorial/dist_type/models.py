from sqlalchemy import Identity, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ...common.constants import Table
from ...db import Base


class DistTypeModel(Base):
    __tablename__ = Table.DistributionType.table_name
    code: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True, index=True)
    word_code: Mapped[int] = mapped_column(Integer, nullable=False)
