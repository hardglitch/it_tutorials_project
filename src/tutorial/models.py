from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.constants.constants import Table
from src.db import Base


class Tutorial(Base):
    __tablename__ = Table.Tutorial.table_name
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    type_code: Mapped[int] = mapped_column(Integer, ForeignKey(Table.Type.type_code))
    theme_code: Mapped[int] = mapped_column(Integer, ForeignKey(Table.Theme.theme_code))
    description: Mapped[str] = mapped_column(String(length=10000), nullable=False)
    language_code: Mapped[int] = mapped_column(Integer, ForeignKey(Table.Language.language_code))
    source_link: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    share_type_code: Mapped[int] = mapped_column(Integer, ForeignKey(Table.DistributionType.distribution_type_code))
    who_added_id: Mapped[int] = mapped_column(Integer, ForeignKey(Table.User.user_id))
