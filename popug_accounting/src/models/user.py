from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    Integer,
    String,
    Table,
    text,
)

from popug_schema_registry.models.v1.task_created_event_schema import UserRoles
from popug_sdk.db import mapper_registry


@mapper_registry.mapped
@dataclass
class User:
    __table__ = Table(
        "users",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("public_id", String(50), unique=True, nullable=False),
        Column(
            "username",
            String(50),
            nullable=False,
            default="",
            server_default=text("''"),
        ),
        Column(
            "email",
            String(100),
            nullable=False,
            default="",
            server_default=text("''"),
        ),
        Column("role", Enum(UserRoles)),
        Column(
            "is_deleted",
            Boolean,
            nullable=False,
            default=False,
            server_default=text("false"),
        ),
    )

    public_id: str
    role: UserRoles | None = None
    username: str = ""
    email: str = ""
    id: int = field(init=False)
    is_deleted: bool = False

    @classmethod
    def get_updatable_fields(cls) -> list[str]:
        return ["username", "role", "email", "is_deleted"]
