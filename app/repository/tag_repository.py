from contextlib import AbstractContextManager
from typing import Callable, Generator
from app.models.tag import Tag
from sqlalchemy.orm import Session

from app.repository.base_repository import BaseRepository


class TagRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., Generator[Session, None, None]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Tag)

