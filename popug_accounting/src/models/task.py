from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    Text,
    text,
)

from popug_sdk.db import mapper_registry


@mapper_registry.mapped
@dataclass
class Task:
    __table__ = Table(
        "tasks",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("public_id", String(50), unique=True, nullable=False),
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
    )

    public_id: str
    title: str = ""
    short_title: str = ""
    id: int = field(init=False)
    description: str = ""
    jira_id: int = None

    @classmethod
    def get_updatable_fields(cls) -> list[str]:
        return ["title", "description"]

    @property
    def long_title(self) -> str:
        return (
            f"[{self.jira_id}]-{self.short_title})"
            if self.jira_id
            else self.title
        )
