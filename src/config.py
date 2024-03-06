from typing import Optional

from pydantic_settings import BaseSettings

VERSION = "0.00.01"
BACKEND_CORS_ORIGINS = ["*"]
METHODS = ["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
HEADERS = ["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
           "Authorization"]


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


settings = AppSettings()
