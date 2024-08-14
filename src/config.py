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

dotenv.load_dotenv('.env')

MANAGER_SECRET = os.getenv("MANAGER_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")
