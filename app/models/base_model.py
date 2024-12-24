from datetime import datetime

from sqlalchemy import Integer, Column, DateTime, func
from sqlalchemy.orm import declared_attr
from sqlalchemy import inspect
import re

from app.models import Base

def resolve_table_name(name: str) -> str:
    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    @declared_attr
    def __tablename__(self) -> str:
        return resolve_table_name(self.__name__)

    def dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
