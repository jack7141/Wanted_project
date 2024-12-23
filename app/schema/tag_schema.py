from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel

from app.util.schema import AllOptional


class BaseTag(BaseModel, metaclass=AllOptional):
    id: int
    tag_name_ko: str
    tag_name_en: str
    tag_name_ja: str

    class Config:
        orm_mode = True
