from pydantic import BaseModel
from decimal import Decimal


class GoodCreate(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    amount: int
    rate: Decimal
    seller_id: int