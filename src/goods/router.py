from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from .schemas import GoodCreate
from database import get_async_session
from goods.models import good


router = APIRouter(
    prefix="/goods",
    tags = ["Goods"]
)

@router.post("/")
async def add_good(new_good: GoodCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(good).values(**new_good.model_dump())
    await session.execute(stmt)
    await session.commit()