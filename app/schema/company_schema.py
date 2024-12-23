from datetime import datetime
from typing import List, Optional, Union, Literal, Any

from pydantic import BaseModel, root_validator

from app.schema.base_schema import FindBase, APIResponse
from app.schema.tag_schema import BaseTag
from app.util.schema import AllOptional


class BaseCompany(BaseModel, metaclass=AllOptional):
    id: int
    company_name_ko: str
    company_name_en: str
    company_name_ja: str


class FindCompany(FindBase, BaseCompany, metaclass=AllOptional): ...


class CompanyResp(BaseModel, metaclass=AllOptional):
    # class TagItems(BaseModel, metaclass=AllOptional):
    #     tag_name_ko: str
    #     tag_name_en: str
    #     tag_name_ja: str

    company_name_ko: str
    company_name_en: str
    company_name_ja: str
    # tags: List[TagItems]
    
    def dict(self, **kwargs) -> dict:
        return super().dict(**kwargs)