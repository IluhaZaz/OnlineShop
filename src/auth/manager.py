from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, schemas, models

from auth.utils import User, get_user_db
from config import MANAGER_SECRET as SECRET

from tasks.email_task import send_email_report_dashboard, get_email_template_dashboard


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} {user.email} has registered.")
        content: str = f"<div>Dear {user.name}, you have been registred in our online shop</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                            theme="Successful registration",
                                                            content=content)
        send_email_report_dashboard.delay(email)

    async def on_after_login(self, user: User, request: Request | None = None, response: Response | None = None) -> None:
        print(f"User {user.id} {user.email} has logined.")

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None):
        print(f"User {user.id} {user.email} has requested password reset.")
        content: str = f"<div>Dear {user.name}, use this token to reset your password:</div><div>{token}</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                            theme="Password reset",
                                                            content=content)
        send_email_report_dashboard.delay(email)
    
    async def on_after_reset_password(self, user: User, request: Request | None = None) -> None:
        print(f"User {user.id} {user.email} has reseted password.")
        content: str = f"<div>Dear {user.name}, your password has been reseted</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                            theme="Password reset",
                                                            content=content)
        send_email_report_dashboard.delay(email)

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None) -> None:
        print(f"User {user.id} {user.email} has requested email verification.")
        content: str = f"<div>Dear {user.name}, use this token to verify your email:</div><div>{token}</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                            theme="Email verification",
                                                            content=content)
        send_email_report_dashboard.delay(email)

    async def on_after_verify(self, user: User, request: Request | None = None) -> None:
        print(f"User {user.id} {user.email} has been verified.")
        content: str = f"<div>Dear {user.name}, your email has been verified"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                            theme="Email verification",
                                                            content=content)
        send_email_report_dashboard.delay(email)
        
    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)