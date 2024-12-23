from contextlib import AbstractContextManager
from typing import Callable, Generator

from app.models.company import Company
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.repository.base_repository import BaseRepository

from app.core.exception import NotFoundError


class CompanyRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
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