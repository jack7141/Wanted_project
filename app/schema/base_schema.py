import typing
from datetime import datetime
from typing import List, Optional, Union

from fastapi.responses import JSONResponse
from typing import Any, Optional, Type, TypeVar
from pydantic import BaseModel


class ModelBaseInfo(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime


class FindBase(BaseModel):
    ordering: Optional[str]
    page: Optional[int]
    page_size: Optional[Union[int, str]]


class SearchOptions(FindBase):
    total_count: Optional[int]


class FindResult(BaseModel):
    founds: Optional[List]
    search_options: Optional[SearchOptions]


class FindDateRange(BaseModel):
    created_at__lt: str
    created_at__lte: str
    created_at__gt: str
    created_at__gte: str


class Blank(BaseModel):
    pass


class APIResponse(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


    def dict(self, by_alias=True, **kwargs):
        return super().dict(by_alias=by_alias, **kwargs)
