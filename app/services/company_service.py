from app.repository.company_repository import CompanyRepository
from app.services.base_service import BaseService


class CompanyService(BaseService):
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository
        super().__init__(company_repository)
