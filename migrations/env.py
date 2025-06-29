from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config, AsyncConnection

from core.config import DATABASE_URL
from core.models import Base


config = context.config
fileConfig(config.config_file_name)


target_metadata = Base.metadata


def get_engine():
    return async_engine_from_config(
        {
            "sqlalchemy.url": DATABASE_URL,
            "sqlalchemy.poolclass": pool.NullPool,
        },
        prefix="sqlalchemy.",
        future=True,
    )


async def run_migrations_online() -> None:
    """Запуск миграций в «online»-режиме с AsyncEngine."""

    connectable = get_engine()

    async with connectable.connect() as connection:  # type: AsyncConnection
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,        # ловит изменения типов колонок
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    raise RuntimeError("Offline-режим не используется — запускай alembic online")
else:
    asyncio.run(run_migrations_online())
