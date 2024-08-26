from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update
from decimal import Decimal

from .schemas import GoodRead, GoodCreate
from database import get_async_session
from auth.models import User
from goods.models import good
from auth.models import user as user_table
from auth.schemas import SellerInfo
from auth.schemas import UserRead
from goods.schemas import Rate, Pagination


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

@router.post("/add_good")
async def add_good(new_good: GoodCreate, 
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(verified_users)
                   ):
    
    if user.role_id != 2:
        raise HTTPException(status_code=400, detail=
                            {
                                "status": "error",
                                "detail": "you need to be a seller",
                                "data": None
                            }
                            )
    
    new_good.seller_id = user.id
    stmt = insert(good).values(**new_good.model_dump(exclude="id"))
    await session.execute(stmt)
    await session.commit()

    res = await session.execute(good.select().order_by(good.c.id.desc()).limit(1))
    res = GoodRead.model_validate(res.first(), from_attributes=True)

    return {
        "status": "ok",
        "detail": "good added",
        "data": res.model_dump()
    }


@router.get("/get_goods", response_model=dict)
async def get_goods(session: AsyncSession = Depends(get_async_session), 
                    p: Pagination = Depends(),
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
    query = query.offset(p.offset*p.limit).limit(p.limit)
    
    res = await session.execute(query)
    res = res.all()
    res = [GoodRead.model_validate(line, from_attributes=True).model_dump() for line in res]
    return {
        "status": "ok",
        "detail": "got goods",
        "data": res
    }


@router.patch("/update_good")
async def update_good(id: int, 
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(verified_users),
                      name: str = None,
                      description: str = None,
                      price: Decimal = None,
                      amount: int = None
                    ):
    
    query = select(good).where(good.c.id == id)
    curr_good = await session.execute(query)
    curr_good = curr_good.all()[0]
    curr_good = GoodRead.model_validate(curr_good, from_attributes=True)
    
    if curr_good.seller_id != user.id:
        raise HTTPException(status_code=400, detail=
                            {
                                "status": "error",
                                "detail": "that's not your good",
                                "data": None
                            }
                            )
    
    stmt = update(good)
    if name:
        stmt = stmt.values(name=name)
    if description:
        stmt = stmt.values(description=description)
    if price:
        stmt = stmt.values(price=price)
    if amount:
        stmt = stmt.values(amount=amount)
    stmt = stmt.where(good.c.id == curr_good.id)

    await session.execute(stmt)
    await session.commit()

    res = await session.execute(select(good).where(good.c.id == id))
    res = GoodRead.model_validate(res.first(), from_attributes=True)

    return {
        "status": "ok",
        "detail": "good updated",
        "data": res.model_dump()
    }
    

@router.delete("/delete_good")
async def delete_good(id: int, 
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(verified_users)
                      ):
    
    query = select(good).where(good.c.id == id)
    curr_good = await session.execute(query)
    curr_good = curr_good.all()[0]
    curr_good = GoodRead.model_validate(curr_good, from_attributes=True)
    if curr_good.seller_id != user.id:
        raise HTTPException(status_code=400, detail=
                            {
                                "status": "error",
                                "detail": "that's not your good",
                                "data": None
                            }
                            )
    
    stmt = delete(good).where(good.c.id == curr_good.id)
    await session.execute(stmt)
    await session.commit()

    return {
                "status": "ok",
                "detail": "good deleted",
                "data": curr_good.model_dump()
            }


@router.post("/become_seller")
async def become_seller(
    your_data: SellerInfo,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(verified_users)
                      ):
    user = await session.get(User, user.id)
    user.role_id = 2
    user.seller_data = your_data.model_dump()

    await session.commit()
    
    return {
                "status": "ok",
                "detail": "now you are a seller",
                "data": UserRead.model_validate(user, from_attributes=True).model_dump()
            }


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
        raise HTTPException(status_code=400, detail={
                                "status": "error",
                                "detail": "you can't rate your good",
                                "data": None
                            }
                            )
    if user.id in good_obj.rated_by:
        raise HTTPException(status_code=400, detail={
                                "status": "error",
                                "detail": "you can't rate good twice",
                                "data": None
                            }
                            )

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

    rated_good = await session.execute(select(good).where(good.c.id == good_id))
    rated_good = rated_good.first()

    return {
                "status": "ok",
                "detail": "good rated",
                "data": GoodRead.model_validate(rated_good, from_attributes=True).model_dump()
            }