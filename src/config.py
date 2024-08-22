import os
import dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_PASS: str
    DB_PORT: str
    DB_USER: str

    model_config = SettingsConfigDict()

db_settings = DbSettings()

class DbTestSettings(BaseSettings):
    DB_HOST_TEST: str
    DB_NAME_TEST: str
    DB_PASS_TEST: str
    DB_PORT_TEST: str
    DB_USER_TEST: str

    model_config = SettingsConfigDict()

db_test_settings = DbTestSettings()

dotenv.load_dotenv('.env')

MANAGER_SECRET = os.getenv("MANAGER_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")

SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_USER = os.getenv("SMTP_USER")
