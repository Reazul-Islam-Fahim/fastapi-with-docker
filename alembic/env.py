# import asyncio
# from logging.config import fileConfig

# from sqlalchemy.ext.asyncio import async_engine_from_config, AsyncEngine
# from alembic import context

# # Import your Base and models
# from database.db import Base
# # from models.users.users import Users  
# # from models.categories.categories import Categories 
# from models import * 

# # This is the Alembic Config object, which provides
# # access to the values within the .ini file in use.
# config = context.config

# # Configure logging
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # Set the target metadata
# target_metadata = Base.metadata

# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode."""
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#         compare_type=True,
#         compare_server_default=True,
#     )

#     with context.begin_transaction():
#         context.run_migrations()

# def do_run_migrations(connection):
#     context.configure(
#         connection=connection,
#         target_metadata=target_metadata,
#         compare_type=True,
#         compare_server_default=True,
#         include_schemas=True,
#         render_as_batch=True,
#     )

#     with context.begin_transaction():
#         context.run_migrations()

# async def run_migrations_online() -> None:
#     """Run migrations in 'online' mode."""
#     connectable = async_engine_from_config(
#         config.get_section(config.config_ini_section, {}),
#         prefix="sqlalchemy.",
#         poolclass=None,
#     )

#     async with connectable.connect() as connection:
#         await connection.run_sync(do_run_migrations)
#         await connection.commit()  # Explicit commit

#     await connectable.dispose()

# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     asyncio.run(run_migrations_online())






import asyncio
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config, AsyncEngine
from alembic import context

from database.db import Base
from models import *  # Import all your models so Alembic sees them

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Your SQLAlchemy metadata (used for autogeneration)
target_metadata = Base.metadata


# --- Offline migrations (text-based SQL) ---
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url").replace("+asyncpg", "")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# --- Synchronous engine for autogenerate ---
def run_migrations_online() -> None:
    """Run migrations in 'online' mode using sync engine (for autogenerate)."""
    url = config.get_main_option("sqlalchemy.url").replace("+asyncpg", "")

    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# --- Optional: Async engine (for running upgrades manually with asyncpg) ---
async def run_async_migrations() -> None:
    """Optional: Async version (not used by autogenerate)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=None,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(run_migrations_with_connection)
        await connection.commit()

    await connectable.dispose()


# --- Shared logic for async engine (optional) ---
def run_migrations_with_connection(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# --- Entry point ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()  # Always use sync for Alembic
