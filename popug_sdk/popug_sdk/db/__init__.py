from contextlib import contextmanager
from typing import Any

from sqlalchemy import create_engine as _engine_create
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

from popug_sdk.conf import settings
from popug_sdk.db.registry import mapper_registry

__all__ = (
    "create_engine",
    "create_session",
    "init_db",
    "mapper_registry",
)


_engine: Engine | None = None
_Session: sessionmaker | None = None


def create_engine() -> Engine:
    global _engine

    if not _engine:
        _engine = _engine_create(settings.database_dsn, pool_pre_ping=True)

    return _engine


def init_db() -> sessionmaker:
    global _Session
    create_engine()

    if not _Session:
        _Session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine,
            expire_on_commit=False,
        )

        return _Session


@contextmanager
def create_session(session: Session | None = None, **kwargs: Any) -> Session:
    if not session:
        _session = init_db()

        with _session(**kwargs) as session:
            yield session
    else:
        yield session
