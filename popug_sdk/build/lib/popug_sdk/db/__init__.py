from contextlib import contextmanager

from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    sessionmaker,
    Session,
)
from sqlalchemy import create_engine as _engine_create

from popug_sdk.conf import settings
from popug_sdk.db.base_class import BaseModel

__all__ = (
    "create_session",
    "BaseModel",
    "init_db",
    "create_engine",
)


_engine: Engine | None = None
_Session: sessionmaker | None = None


def create_engine() -> Engine:
    global _engine

    if not _engine:
        _engine = _engine_create(settings.database_dsn, pool_pre_ping=True)

    return _engine


def init_db():
    global _Session
    create_engine()

    if not _Session:
        _Session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine,
            expire_on_commit=False
        )


@contextmanager
def create_session(session=None, **kwargs) -> Session:
    init_db()

    if not session:
        with _Session(**kwargs) as session:
            yield session
    else:
        yield session
