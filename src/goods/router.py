from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update
from decimal import Decimal

from .schemas import GoodRead, GoodCreate
from database import get_async_session, User
from goods.models import good
from auth.models import user as user_table
from auth.schemas import SellerInfo
from goods.schemas import Rate


from fastapi_users.fastapi_users import FastAPIUsers

from auth.auth_back import auth_backend
from auth.manager import get_user_manager


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

@router.get("/", response_model=list[GoodRead])
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
    curr_good = GoodRead.model_validate(curr_good, from_attributes=True)
    
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
    curr_good = GoodRead.model_validate(curr_good, from_attributes=True)
    if curr_good.seller_id != user.id:
        raise HTTPException(402, "that's not your good")
    
    stmt = delete(good).where(good.c.id == curr_good.id)
    await session.execute(stmt)
    await session.commit()

@router.post("/sell")
async def become_seller(
    your_data: SellerInfo,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(verified_users)
                      ):
    stmt = update(user_table).values(role_id = 2, seller_data = your_data.model_dump()).where(user_table.c.id == user.id)
    await session.execute(stmt)
    await session.commit()

@router.post("/rate")
async def rate(good_id: int,
                rate: Rate,
                session: AsyncSession = Depends(get_async_session),
                user: User = Depends(verified_users)
    ):

    good_obj = await session.execute(select(good).where(good.c.id == good_id))
    good_obj = good_obj.all()[0]
    good_obj = GoodRead.model_validate(good_obj, from_attributes=True)

    if good_obj.seller_id == user.id:
        raise HTTPException(400, "you can't rate your good")
    if user.id in good_obj.rated_by:
        raise HTTPException(400, "you can't rate good twice")

    rate.good_id = good_id
    stmt = update(good).values(rate_cnt = good.c.rate_cnt + 1, 
                               rate_sum = good.c.rate_sum + rate.rate,
                               rate = (good.c.rate_sum + rate.rate)/(good.c.rate_cnt + 1),
                               rated_by = good.c.rated_by + [user.id]
                               ).where(good.c.id == good_id)
    await session.execute(stmt)
    
    user.comments.append(rate.model_dump())

    stmt = update(user_table).values(comments=user.comments).where(user_table.c.id == user.id)
    await session.execute(stmt)

    await session.commit()