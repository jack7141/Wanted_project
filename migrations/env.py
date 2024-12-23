import os
import sys
import importlib
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel
from dotenv import load_dotenv

from app import models

load_dotenv()

# Add the app directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

# Alembic Config object
config = context.config

# Use DATABASE_URI dynamically if not set in alembic.ini
from app.core.config import configs  # Import your dynamic configurations
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", configs.DATABASE_URI)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Dynamically import all models from app.models
def include_models():
    models_dir = os.path.join(os.path.dirname(__file__), "../app/models")
    for file in os.listdir(models_dir):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"app.models.{file[:-3]}"
            importlib.import_module(module_name)

include_models()

# Set target_metadata
target_metadata = models.Base.metadata


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            dialect_opts={"paramstyle": "named"},
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    raise NotImplementedError("Offline migrations are not supported in this setup")
else:
    run_migrations_online()