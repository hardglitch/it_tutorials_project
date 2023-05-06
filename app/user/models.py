from pydantic import EmailStr
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.common.constants import Credential, Table
from app.db import Base


class UserModel(Base):
    __tablename__ = Table.User.table_name
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(length=256), nullable=False, unique=True, index=True)
    email: Mapped[EmailStr] = mapped_column(String(length=320), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    credential: Mapped[int] = mapped_column(Integer, default=Credential.user)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    rating: Mapped[int] = mapped_column(Integer, default=0)
