"""Migration script for database.

Description:
- This script is used to run migrations for database.

"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel import MetaData, SQLModel

from alembic.context import (
    begin_transaction,
    config,
    configure,
    is_offline_mode,
    run_migrations,
)
from fastapi_boilerplate.core.config import settings
from fastapi_boilerplate.core.load_models import load_all_models

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(fname=config.config_file_name)

# Set the database URL in the config object
config.set_main_option(
    name="sqlalchemy.url", value=str(settings.SQLALCHEMY_DATABASE_URI)
)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata: MetaData = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an
    Engine is acceptable here as well. By skipping the Engine creation we don't
    even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.

    """
    url: str | None = config.get_main_option(name="sqlalchemy.url")
    configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with begin_transaction():
        run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with the given connection.

    :Description:
    - This function is used to run migrations with the given connection.

    :Args:
    - `connection`: (Connection) The connection to use for running migrations.
    **(Required)**

    :Returns:
    - `None`

    """
    configure(connection=connection, target_metadata=target_metadata)

    with begin_transaction():
        # Load all models before running migrations
        load_all_models()

        run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode using async engine.

    :Description:
    - In this scenario we need to create an Engine and associate a connection
    with the context.

    """
    connectable: AsyncEngine = async_engine_from_config(
        configuration=config.get_section(
            name=config.config_ini_section, default={}
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(fn=do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(main=run_async_migrations())


if is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
