from sqlalchemy import Table, Column, ForeignKey, Integer, String, MetaData, Numeric, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

meta_data = MetaData()

role = Table(
    "role",
    meta_data,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON)
)

user = Table(
    "user",
    meta_data,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("role_id", Integer, ForeignKey(role.c.id, ondelete="CASCADE")),

    Column("hashed_password", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)

product = Table(
    "product",
    meta_data,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("price", Numeric(15, 2), nullable=False),
    Column("amount", Integer, nullable=False),
    Column("rate", Numeric(3, 2), nullable=False),
    Column("seller_id", Integer, ForeignKey(user.c.id))
)

Base: DeclarativeMeta = declarative_base()

class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey(role.c.id))

    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )