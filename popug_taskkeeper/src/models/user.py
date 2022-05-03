from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

from constants import UserRoles
from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    Integer,
    String,
    Table,
    text,
)

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
        Column("role", Enum(UserRoles)),
        Column(
            "is_deleted",
            Boolean,
            nullable=False,
            default=False,
            server_default=text("false"),
        ),
    )

    role: UserRoles
    username: str = ""
    public_id: str = ""
    id: int = field(init=False)
    is_deleted: bool = False

    @classmethod
    def get_updatable_fields(cls) -> list[str]:
        return ["username", "role", "is_deleted"]
