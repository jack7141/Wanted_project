from dependency_injector import containers, providers

from app.core.config import configs
from app.core.database import Database
from app.repository.company_repository import CompanyRepository
from app.repository.tag_repository import TagRepository
from app.services.company_service import CompanyService
from app.services.tag_service import TagService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.tag",
            "app.api.v1.endpoints.company",
        ]
    )
    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    tag_repository = providers.Factory(TagRepository, session_factory=db.provided.session)
    company_repository = providers.Factory(CompanyRepository, session_factory=db.provided.session)

    tag_service = providers.Factory(TagService, tag_repository=tag_repository)
    company_service = providers.Factory(CompanyService, company_repository=company_repository)
