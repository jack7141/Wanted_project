from sqlalchemy.orm import joinedload

from app.core.exception import NotFoundError
from app.repository.company_repository import CompanyRepository
from app.services.base_service import BaseService

class CompanyService(BaseService):
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository
        super().__init__(company_repository)

    def get_company_by_language(self, company_id, field, x_wanted_language):
        query = self.company_repository.filter_across_languages(company_id)
        tags_field = "tags"
        result = {
            "company_name": getattr(query, field, None),
            "tags": [
                getattr(tag, f"tag_name_{x_wanted_language}", None)
                for tag in getattr(query, tags_field, [])
            ],
        }
        return result