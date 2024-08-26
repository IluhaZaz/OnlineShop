import os
import dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_PASS: str
    DB_PORT: str
    DB_USER: str

    model_config = SettingsConfigDict()

db_settings = DbSettings()

class DbTestSettings(BaseSettings):
    DB_HOST_TEST: str|None = Field(default=None)
    DB_NAME_TEST: str|None = Field(default=None)
    DB_PASS_TEST: str|None = Field(default=None)
    DB_PORT_TEST: str|None = Field(default=None)
    DB_USER_TEST: str|None = Field(default=None)

    model_config = SettingsConfigDict()

db_test_settings = DbTestSettings()

dotenv.load_dotenv()

MANAGER_SECRET = os.getenv("MANAGER_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")

SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_USER = os.getenv("SMTP_USER")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
