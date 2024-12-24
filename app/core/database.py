from contextlib import AbstractContextManager, contextmanager
from typing import Any, Generator
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session
from loguru import logger


@as_declarative()
class BaseModel:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Database:
    def __init__(self, db_url: str, debug: bool = False) -> None:
        self._engine = create_engine(db_url, echo=debug)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        try:
            # Check if table exists
            if not self._engine.dialect.has_table(self._engine, "some_table"):
                BaseModel.metadata.create_all(self._engine)
        except Exception as e:
            logger.error(f"Error during database creation: {str(e)}")
            raise

    @contextmanager
    def session(self) -> Generator[Session, None, None]:  # Updated type hint
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()