from typing import Optional

from pydantic_settings import BaseSettings

VERSION = "0.00.01"
BACKEND_CORS_ORIGINS = ["*"]
METHODS = ["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
HEADERS = ["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
           "Authorization"]
CONVENTION = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "hello world app"
    PROJECT_DESCRIPTION: str = "hello world app"
    STAGE: str = "default"
    ENVIRONMENT: str = "local"
    OPENAPI_URL: str = ""
    TELEBOT_TOKEN: Optional[str] = None
    LOG_TG_CHANNEL: Optional[str] = None
    SEND_LOGS: bool = False
    SEND_ERRORS: bool = False
    LOG_DELAY: float = 0.5
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

settings = AppSettings()

DB_HOST = settings.POSTGRES_HOST
DB_PORT = settings.POSTGRES_PORT
DB_NAME = settings.POSTGRES_DB
DB_USER = settings.POSTGRES_USER
DB_PASS = settings.POSTGRES_PASSWORD
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
