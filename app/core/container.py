from dependency_injector import containers, providers

from app.core.config import configs
from app.core.database import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
        ]
    )
    db = providers.Singleton(Database, db_url=configs.DB_URL, sync_db_url=configs.SYNC_DB_URL)
