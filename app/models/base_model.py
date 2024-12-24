from datetime import datetime
from fastapi import HTTPException, Header

from sqlalchemy import Integer, Column, DateTime, func
from sqlalchemy.orm import declared_attr
from sqlalchemy import inspect
import re

from app.models import Base

LANGUAGE_ACTION_MAP = {"ko": "company_name_ko", "en": "company_name_en", "ja": "company_name_ja"}

def get_clean_language(x_wanted_language: str = Header("ko")) -> str:
    language = ''.join(c for c in x_wanted_language if c.isprintable()).strip()

    if language not in ["ko", "en", "ja"]:
        raise HTTPException(status_code=400, detail="Invalid language")

    return language

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
