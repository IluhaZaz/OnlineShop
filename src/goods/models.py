from sqlalchemy import Table, Column, MetaData, ForeignKey, Integer, Numeric, String

from auth.models import user


meta_data = MetaData()

good = Table(
    "good",
    meta_data,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("price", Numeric(15, 2), nullable=False),
    Column("amount", Integer, nullable=False),
    Column("rate", Numeric(3, 2), nullable=False, default=0),
    Column("rate_cnt", Integer, nullable=False, default=0),
    Column("rate_sum", Numeric(3, 2), nullable=False, default=0),
    Column("seller_id", Integer, ForeignKey(user.c.id))
)