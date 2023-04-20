# SQLAlchemy models

from typing import List
from pydantic import EmailStr
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base
from src.constants.constants import Credential, ShareType, Table


class User(Base):
    __tablename__ = Table.User.table_name

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    email: Mapped[EmailStr] = mapped_column(String(length=320), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    credential: Mapped[Credential] = mapped_column(Integer, default=Credential.user)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    rating: Mapped[int] = mapped_column(Integer, default=0)

    tutorial: Mapped[List["Tutorial"]] = relationship(back_populates=Table.Tutorial.who_added)


class Tutorial(Base):
    __tablename__ = Table.Tutorial.table_name

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    theme: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(length=10000), nullable=False)
    language: Mapped[int] = mapped_column(Integer, nullable=False)
    source_link: Mapped[str] = mapped_column(String, nullable=False)
    share_type: Mapped[int] = mapped_column(Integer, default=ShareType.free)
    who_added_id: Mapped[int] = mapped_column(Integer, ForeignKey(Table.User.user_id))

    who_added: Mapped["User"] = relationship(back_populates=Table.User.tutorial)


class Language(Base):
    __tablename__ = Table.Language.table_name

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    abbreviation: Mapped[str] = mapped_column(String(length=3), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    is_ui_lang: Mapped[bool] = mapped_column(Boolean, default=False)


class TutorialTheme(Base):
    __tablename__ = Table.Theme.table_name

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    eng: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=False)
    rus: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=False)
    ukr: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=False)


class TutorialType(Base):
    __tablename__ = Table.Type.table_name

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    eng: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=False)
    rus: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=False)
    ukr: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=False)
