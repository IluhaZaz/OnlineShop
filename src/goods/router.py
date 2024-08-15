from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update
from decimal import Decimal

from .schemas import GoodCreate
from database import get_async_session
from goods.models import good


from fastapi_users.fastapi_users import FastAPIUsers

from auth.auth_back import auth_backend
from auth.manager import get_user_manager
from database import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


router = APIRouter(
    prefix="/goods",
    tags = ["Goods"]
)

current_user = fastapi_users.current_user()
verified_users = fastapi_users.current_user(verified=True)

@router.post("/")
async def add_good(new_good: GoodCreate, 
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(verified_users)
                   ):
    if not user:
        raise HTTPException(400, "you need to be authenticated")
    
    if user.role_id != 2:
        raise HTTPException(401, "you are not a seller")
    
    new_good.seller_id = user.id
    stmt = insert(good).values(**new_good.model_dump(exclude="id"))
    await session.execute(stmt)
    await session.commit()

@router.get("/", response_model=list[GoodCreate])
async def get_goods(session: AsyncSession = Depends(get_async_session), 
                    rate: Decimal = None,
                    name: str = None,
                    price_l: Decimal = None,
                    price_r: Decimal = None
                    ):
    query = select(good)
    if name:
        query = query.where(good.c.name.ilike(name))
    if rate:
        query = query.where(good.c.rate >= rate)
    if price_l:
        query = query.where(good.c.price >= price_l)
    if price_r:
        query = query.where(good.c.price <= price_r)
    
    res = await session.execute(query)
    return res.all()

@router.patch("/")
async def update_good(id: int, 
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(verified_users),
                      name: str = None,
                      description: str = None,
                      price: Decimal = None
                    ):
    if not user:
        raise HTTPException(400, "you need to be authenticated")
    
    query = select(good).where(good.c.id == id)
    curr_good = await session.execute(query)
    curr_good = curr_good.all()[0]
    curr_good = GoodCreate.model_validate(curr_good, from_attributes=True)
    
    if curr_good.seller_id != user.id:
        raise HTTPException(402, "that's not your good")
    
    stmt = update(good)
    if name:
        stmt = stmt.values(name=name)
    if description:
        stmt = stmt.values(description=description)
    if price:
        stmt = stmt.values(price=price)
    stmt = stmt.where(good.c.id == curr_good.id)

    await session.execute(stmt)
    await session.commit()
    

@router.delete("/")
async def delete_good(id: int, 
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(verified_users)
                      ):
    if not user:
        raise HTTPException(400, "you need to be authenticated")
    
    query = select(good).where(good.c.id == id)
    curr_good = await session.execute(query)
    curr_good = curr_good.all()[0]
    curr_good = GoodCreate.model_validate(curr_good, from_attributes=True)
    if curr_good.seller_id != user.id:
        raise HTTPException(402, "that's not your good")
    
    stmt = delete(good).where(good.c.id == curr_good.id)
    await session.execute(stmt)
    await session.commit()

@router.post("/")
async def become_seller():
    pass