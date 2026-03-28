import asyncio
from logging.config import fileConfig
import os
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ИМПОРТИРУЕМ МОДЕЛИ
from app.models import Base 

# 1. Конфигурация Alembic
config = context.config

# 2. Настройка логгирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Переопределяем URL из переменных окружения (Docker передает DATABASE_URL)
# Это лечит ошибку "sqlalchemy.dialects:driver"
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# 4. Указываем метаданные моделей для авто-генерации миграций
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode (Async)."""
    
    # Создаем асинхронный движок
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Alembic работает синхронно внутри асинхронного соединения
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    # Запускаем асинхронную функцию через asyncio
    asyncio.run(run_migrations_online())