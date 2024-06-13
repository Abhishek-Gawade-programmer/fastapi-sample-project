import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import PostgresDsn, computed_field, MySQLDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"

    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    DB_HOST: str
    DB_PORT: str = ""
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str = ""
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:

        return MultiHostUrl.build(
            scheme="mysql",
            username=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            # port=settings.DB_PORT,
            path=settings.DB_NAME,
        )


settings = Settings()  # type: ignore
