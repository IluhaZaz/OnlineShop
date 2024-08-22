from sqlalchemy import Table, Column, ForeignKey, Integer, Numeric, String, ARRAY

from auth.models import user
from database import meta_data

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
    Column("rated_by", ARRAY(Integer), nullable=[False], default=[]),
    Column("seller_id", Integer, ForeignKey(user.c.id))
)