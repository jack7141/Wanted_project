from contextlib import AbstractContextManager
from typing import Callable, Generator

from app.models.company import Company
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.repository.base_repository import BaseRepository

from app.core.exception import NotFoundError

from sqlalchemy import or_


class CompanyRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., Generator[Session, None, None]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Company)


    def read_by_fields(self, eager: bool = False, last: bool = False, **filters):
        with self.session_factory() as session:
            query = session.query(self.model)
            if eager:
                for eager_field in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager_field)))
            for field, value in filters.items():
                query = query.filter(getattr(self.model, field) == value)
            if last:
                query = query.order_by(desc(self.model.id))
            query = query.first()
            if not query:
                raise NotFoundError(detail=f"not found values from Request Filter: {filters}")
            return query

    def filter_by_field(self, field: str, value: str):
        with self.session_factory() as session:
            return session.query(self.model).filter(getattr(self.model, field).ilike(f"%{value}%")).all()

    def filter_across_languages(self, value: str):
        with self.session_factory() as session:
            language_fields = ["company_name_ko", "company_name_en", "company_name_ja"]
            filters = [getattr(self.model, field).ilike(f"%{value}%") for field in language_fields]
            query = session.query(self.model).filter(or_(*filters))

            for eager_field in getattr(self.model, "eagers", []):
                query = query.options(joinedload(getattr(self.model, eager_field)))

            result = query.first()
            if not result:
                raise NotFoundError(detail=f"Company not found for search value: {value}")
            return result