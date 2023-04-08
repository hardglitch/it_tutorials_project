# SQLAlchemy models

from enum import StrEnum
from typing import List, Literal

from pydantic import EmailStr
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base
from src.db_const import Table, Language


class Credential(StrEnum):
    user: str = "user"
    moderator: str = "moderator"
    admin: str = "admin"


class User(Base):
    __tablename__ = Table.User.table_name

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    email: Mapped[EmailStr] = mapped_column(String(length=320), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    credential: Mapped[Credential] = mapped_column(String, nullable=False, default=Credential.user)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    rating: Mapped[int] = mapped_column(Integer, default=0)

    tutorial: Mapped[List["Tutorial"]] = relationship(back_populates=Table.Tutorial.who_added)


class Tutorial(Base):
    __tablename__ = Table.Tutorial.table_name

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    theme: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String(length=10000), nullable=False)
    language: Mapped[Language] = mapped_column(String, nullable=False, default=Table.Tutorial.language)
    source_link: Mapped[str] = mapped_column(String, nullable=False)
    share_type: Mapped[Literal["free", "unfree"]] = mapped_column(String, default="free")
    who_added_id: Mapped[int] = mapped_column(Integer, ForeignKey(".".join([Table.User.table_name, Table.User.id])))

    who_added: Mapped["User"] = relationship(back_populates=Table.User.tutorial)
