from pydantic import BaseModel
from decimal import Decimal

class GoodCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    amount: int
    seller_id: int

class GoodRead(GoodCreate):
    id: int
    rate: Decimal