from sqlalchemy.orm import joinedload

from app.core.exception import NotFoundError
from app.repository.company_repository import CompanyRepository
from app.services.base_service import BaseService

from sqlalchemy import desc

class CompanyService(BaseService):
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository
        super().__init__(company_repository)

    def read_by_fields(self, eager: bool = False, last: bool = False, **filters):
        query = self.company_repository.read_by_fields(eager=eager, last=last, **filters)
        return query