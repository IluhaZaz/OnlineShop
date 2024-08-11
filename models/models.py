from sqlalchemy import Table, Column, ForeignKey, Integer, String, MetaData, Numeric, Boolean, JSON

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
