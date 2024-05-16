"""
Core Configuration Module

Description:
- This module is responsible for core configuration and read values from
environment file.

"""

from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class CoreConfiguration(BaseSettings):
    """
    Core Settings Class

    Description:
    - This class is used to load core configurations from .env file.

    """

    # Database Configuration

    DATABASE: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:  # pylint: disable=C0103
        """
        Database URL

        Description:
        - This property is used to generate database URL.

        """
        return "".join(
            [
                self.DATABASE,
                "://",
                self.DB_USER,
                ":",
                self.DB_PASSWORD,
                "@",
                self.DB_HOST,
                ":",
                str(self.DB_PORT),
                "/",
                self.DB_NAME,
            ]
        )

    # Project Configuration

    CORS_ALLOW_ORIGINS: str
    CORS_ALLOW_METHODS: str
    CORS_ALLOW_HEADERS: str

    PROJECT_TITLE: str = "FastAPI BoilerPlate"
    PROJECT_DESCRIPTION: str = "FastAPI BoilerPlate Backend Documentation"

    VERSION: str = "0.1.0"

    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # JWT Configuration

    ALGORITHM: str
    ACCESS_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Super Admin Configuration

    SUPERUSER_NAME: str
    SUPERUSER_USERNAME: str
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str
    SUPERUSER_ROLE: str
    SUPERUSER_ROLE_DESCRIPTION: str

    # Settings Configuration
    model_config = SettingsConfigDict(env_file=".env")


class TokenType(str, Enum):
    """
    Token Type Enum

    Description:
    - This enum is used to define token type.

    """

    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


core_configuration = CoreConfiguration()  # type: ignore
