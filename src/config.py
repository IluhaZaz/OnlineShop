from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_PASS: str
    DB_PORT: str
    DB_USER: str

    model_config = SettingsConfigDict()

db_settings = DbSettings()