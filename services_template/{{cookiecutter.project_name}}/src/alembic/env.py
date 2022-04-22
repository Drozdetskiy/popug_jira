import asyncio
import os

from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

os.environ.setdefault('SETTINGS_MODULE', 'src.conf')  # noqa

from logging.config import fileConfig

from alembic import context
from src.models import *  # noqa
from sqlalchemy import (
    engine_from_config,
    pool,
)

from popug_sdk.conf import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from popug_sdk.db import BaseModel  # noqa

# target_metadata = mymodel.Base.metadata
target_metadata = BaseModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.database_dsn
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = settings.database_dsn

    connectable = engine_from_config(
            configuration=dict(),
            url=url,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )

    with connectable.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
