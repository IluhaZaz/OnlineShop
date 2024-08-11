from sqlalchemy import Table, Column, ForeignKey, Integer, String, MetaData, Float


meta_data = MetaData()

products = Table(
    "products",
    meta_data,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("price", Float, nullable=False),
    Column("amount", Integer, nullable=False),
    Column("rate", Float, nullable=False),
    Column("seller", Integer, ForeignKey("users.id"))
)

users = Table(
    "users",
    meta_data,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False)
)