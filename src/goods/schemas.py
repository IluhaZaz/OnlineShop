from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class GoodCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    amount: int
    seller_id: int


class GoodRead(GoodCreate):
    id: int
    rate: Decimal
    rated_by: list[int]
    

class Rate(BaseModel):
    good_id: int
    rate: float
    title: Optional[str]
    comment: Optional[str]
    