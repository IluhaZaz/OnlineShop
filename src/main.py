import uvicorn

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.auth_back import auth_backend
from auth.schemas import UserRead, UserCreate
from auth.manager import get_user_manager
from auth.models import User

from goods.router import router as router_goods


app = FastAPI(title="OnlineShop")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth']
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags = ["auth"]
)

app.include_router(router_goods)

if __name__ == "__main__":
    uvicorn.run(
        __name__ + ":app",
        host='127.0.0.1',
        port=8000,
        reload=True
    )