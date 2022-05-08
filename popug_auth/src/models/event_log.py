from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Any

from constants import (
    Entities,
    EventTitles,
    EventTypes,
)
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    Table,
    text,
)
from utils import get_pid

from popug_sdk.db import mapper_registry


@mapper_registry.mapped
@dataclass
class EventLog:
    __table__ = Table(
        "event_log",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "pid", String(50), unique=True, default=get_pid, nullable=False
        ),
        Column(
            "entity",
            Enum(Entities),
            nullable=False,
            default=Entities.USER,
            server_default=text(f"'{Entities.USER.value}'"),
        ),
        Column("title", Enum(EventTitles), nullable=False),
        Column(
            "type",
            Enum(EventTypes),
            nullable=False,
            default=EventTypes.DATA_STREAMING,
            server_default=text(f"'{EventTypes.DATA_STREAMING.value}'"),
        ),
        Column(
            "version",
            Integer,
            nullable=False,
            default=1,
            server_default=text("1"),
        ),
        Column(
            "data",
            JSON,
            nullable=False,
            default=dict,
            server_default=text("'{}'"),
        ),
        Column(
            "processed",
            Boolean,
            nullable=False,
            default=False,
            server_default=text("false"),
        ),
        Column(
            "created_at",
            DateTime,
            nullable=False,
            default=datetime.utcnow,
            server_default=text("(now() at time zone 'utc')"),
        ),
        Column(
            "updated_at",
            DateTime,
            nullable=False,
            default=datetime.utcnow,
            server_default=text("(now() at time zone 'utc')"),
            onupdate=datetime.utcnow,
        ),
    )

    title: EventTitles
    id: int = field(init=False)
    pid: str = field(default_factory=get_pid)
    entity: Entities = Entities.USER
    type: EventTypes = EventTypes.DATA_STREAMING
    version: int = 1
    data: dict[str, Any] = field(default_factory=dict)
    processed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
