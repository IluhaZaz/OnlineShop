from fastapi_users import schemas
from typing import Optional
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    name: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    email: str
    name: str
    role_id: int
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str] = None
    role_id: Optional[int] = None
    password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

class SellerInfo(BaseModel):
    full_name: str
    certificate_num: int
    