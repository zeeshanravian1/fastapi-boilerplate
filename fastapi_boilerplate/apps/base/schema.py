"""
Base Read Pydantic Schema

Description:
- This module contains base read schema used by API.

"""

from datetime import datetime

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from .configuration import base_configuration


class BaseReadSchema(BaseModel):
    """
    Base Read Schema

    Description:
    - This schema is used to validate base data returned by API.

    """

    id: int = Field(examples=[base_configuration.ID])
    created_at: datetime = Field(examples=[base_configuration.CREATED_AT])
    updated_at: datetime | None = Field(
        examples=[base_configuration.UPDATED_AT]
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class BasePaginationReadSchema(BaseModel):
    """
    Base Pagination Read Schema

    Description:
    - This schema is used to validate base pagination data returned by API.

    """

    total_records: int = Field(
        ge=0, examples=[base_configuration.TOTAL_RECORDS]
    )
    total_pages: int = Field(ge=0, examples=[base_configuration.TOTAL_PAGES])
    page: int = Field(ge=1, examples=[base_configuration.PAGE])
    limit: int = Field(ge=0, examples=[base_configuration.LIMIT])
    records: list = Field(examples=[])

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )
