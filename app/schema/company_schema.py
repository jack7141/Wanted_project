from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel

from app.schema.base_schema import FindBase
from app.util.schema import AllOptional


class BaseCompany(BaseModel):
    id: str
    company_name_ko: str
    company_name_en: str
    company_name_ja: str

    class Config:
        orm_mode = True

class FindBCompany(FindBase, BaseCompany, metaclass=AllOptional): ...
