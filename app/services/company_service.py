from sqlalchemy.orm import joinedload

from app.core.exception import NotFoundError
from app.repository.company_repository import CompanyRepository
from app.services.base_service import BaseService

from sqlalchemy import desc

class CompanyService(BaseService):
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository
        super().__init__(company_repository)

    def get_company_by_language(self, eager: bool = False, last: bool = False, x_wanted_language="ko", **filters):
        query = self.company_repository.read_by_fields(eager=eager, last=last, **filters)
        company_name_field = f"company_name_{x_wanted_language}"
        tags_field = "tags"
        result = {
            "company_name": getattr(query, company_name_field, None),
            "tags": [
                getattr(tag, f"tag_name_{x_wanted_language}", None)
                for tag in getattr(query, tags_field, [])
            ],
        }
        return result