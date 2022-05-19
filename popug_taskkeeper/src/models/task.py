from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
    field,
)
from datetime import datetime

from dto.task import TaskDTO
from dto.user import UserDTO
from models.user import User
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    text,
)
from sqlalchemy.orm import relationship
from utils import get_public_id

from popug_schema_registry.models.v1.task_created_event_schema import (
    TaskStatus,
)
from popug_sdk.db import mapper_registry


@mapper_registry.mapped
@dataclass
class Task:
    __table__ = Table(
        "tasks",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "public_id",
            String(50),
            unique=True,
            default=get_public_id,
            nullable=False,
        ),
        Column(
            "title",
            String(50),
            nullable=False,
            default="",
            server_default=text("''"),
        ),
        Column(
            "short_title",
            String(50),
            nullable=False,
            default="",
            server_default=text("''"),
        ),
        Column("jira_id", Integer),
        Column(
            "description",
            Text,
            nullable=False,
            default="",
            server_default=text("''"),
        ),
        Column(
            "status",
            Enum(TaskStatus),
            default=TaskStatus.OPEN,
            nullable=False,
            server_default=text(f"'{TaskStatus.OPEN.value}'"),
        ),
        Column("assignee_id", ForeignKey("users.id")),
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

    title: str = ""
    short_title: str = ""
    jira_id: int | None = None
    id: int = field(init=False)
    public_id: str = field(default_factory=get_public_id)
    description: str = ""
    status: TaskStatus = field(default=TaskStatus.OPEN)
    assignee_id: int | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    assignee: User | None = field(init=False)

    __mapper_args__ = {  # type: ignore
        "properties": {"assignee": relationship("User")}
    }

    def to_dto(self) -> TaskDTO:
        data = asdict(self)

        assignee_data = data["assignee"]
        if assignee_data:
            data["assignee"] = UserDTO(**data["assignee"])

        data["title"] = self.long_title
        data.pop("short_title", None)
        data.pop("jira_id", None)

        return TaskDTO(**data)

    @property
    def long_title(self) -> str:
        return (
            f"[{self.jira_id}]-{self.short_title})"
            if self.jira_id
            else self.title
        )
