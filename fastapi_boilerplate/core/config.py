"""Core Configuration Module.

Description:
- This module is responsible for core configuration and read values from
environment file.

"""

import secrets
import warnings
from typing import Annotated, Literal, Self

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    SecretStr,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from .helper import parse_cors


class Settings(BaseSettings):
    """Core Settings Class.

    :Description:
    - This class is used to define core settings for application.

    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Database Configuration

    DATABASE: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(  # pylint: disable=invalid-name
        self,
    ) -> PostgresDsn:
        """SQLAlchemy Database URI.

        :Description:
        - This property is used to return SQLAlchemy database URI.

        """
        return MultiHostUrl.build(  # type: ignore[return-value]
            scheme=self.DATABASE,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    # Project Configuration

    PROJECT_TITLE: str
    PROJECT_DESCRIPTION: str
    SENTRY_DSN: HttpUrl | None = None
    API_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    FRONTEND_HOST: str

    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    ENVIRONMENT: Literal[
        "local", "development", "testing", "staging", "production"
    ] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(func=parse_cors)
    ] = []
    BACKEND_CORS_METHODS: Annotated[
        list[str] | str, BeforeValidator(func=parse_cors)
    ] = []
    BACKEND_CORS_HEADERS: Annotated[
        list[str] | str, BeforeValidator(func=parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        """All Cors Origins.

        :Description:
        - This property is used to return all cors origins.

        """
        return [
            str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS
        ] + [self.FRONTEND_HOST]

    # JWT Configuration

    ALGORITHM: str
    SECRET_KEY: str = secrets.token_urlsafe(nbytes=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # SMTP Configuration

    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_EMAIL: EmailStr
    SMTP_USER: str | None = None
    SMTP_PASSWORD: SecretStr
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    EMAILS_FROM_NAME: EmailStr | None = None
    EMAIL_RESET_TOKEN_EXPIRE_MINUTES: int = 5

    @model_validator(mode="after")
    def _set_default_smtp_user(self) -> Self:
        if not self.SMTP_USER:
            # pylint: disable=invalid-name
            self.SMTP_USER = self.SMTP_EMAIL

        return self

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            # pylint: disable=invalid-name
            self.EMAILS_FROM_NAME = self.PROJECT_TITLE

        return self

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        """Emails Enabled.

        :Description:
        - This property is used to check if emails are enabled

        """
        return bool(self.SMTP_HOST and self.SMTP_EMAIL)

    # Twilio Configuration

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    # Super Admin Configuration

    SUPERUSER_NAME: str
    SUPERUSER_EMAIL: EmailStr
    SUPERUSER_PASSWORD: str
    SUPERUSER_ROLE: str
    SUPERUSER_ROLE_DESCRIPTION: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SUPERUSER_USERNAME(  # pylint: disable=invalid-name
        self,
    ) -> str:
        """Superuser Username.

        :Description:
        - This property is used to return superuser username.

        """
        return self.SUPERUSER_EMAIL.split(sep="@")[0]

    def _check_default_secret(self, var_name: str, value: str) -> None:
        if value == "changethis":
            message: str = (
                f'Value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )

            if self.ENVIRONMENT == "local":
                warnings.warn(message=message, stacklevel=1)

            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret(
            var_name="DB_PASSWORD", value=self.DB_PASSWORD
        )
        self._check_default_secret(
            var_name="SECRET_KEY", value=self.SECRET_KEY
        )
        self._check_default_secret(
            var_name="SUPERUSER_PASSWORD", value=self.SUPERUSER_PASSWORD
        )

        return self


settings = Settings()  # type: ignore[call-arg]
