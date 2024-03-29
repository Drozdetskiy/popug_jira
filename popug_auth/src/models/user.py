from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Optional

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

from popug_schema_registry.models.v1.task_created_event_schema import UserRoles
from popug_sdk.db import mapper_registry


@mapper_registry.mapped
@dataclass
class User:
    __table__ = Table(
        "user",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "public_id",
            String(50),
            unique=True,
            default=get_public_id,
            nullable=False,
        ),
        Column("username", String(50), nullable=False),
        Column(
            "email",
            String(100),
            nullable=False,
            unique=True,
        ),
        Column(
            "role",
            Enum(UserRoles),
            nullable=False,
            default=UserRoles.EMPLOYEE,
            server_default=text(f"'{UserRoles.EMPLOYEE.value}'"),
        ),
        Column("beak_shape", String(100), nullable=False, unique=True),
    )

    username: str
    email: str
    beak_shape: str
    id: int = field(init=False)
    public_id: str = field(default_factory=get_public_id)
    role: UserRoles = field(default=UserRoles.EMPLOYEE)

    @property
    def refresh_token(self) -> Optional[UserRefreshToken]:
        raise NotImplementedError

    __mapper_args__ = {  # type: ignore
        "properties": {
            "refresh_token": relationship(
                "UserRefreshToken", back_populates="user"
            )
        }
    }


@mapper_registry.mapped
@dataclass
class UserRefreshToken:
    __table__ = Table(
        "user_refresh_token",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user.id"), unique=True),
        Column("refresh_token", Text, nullable=False),
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

    user_id: int
    refresh_token: str
    id: int = field(init=False)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def user(self) -> User:
        raise NotImplementedError

    __mapper_args__ = {  # type: ignore
        "properties": {
            "user": relationship(User, back_populates="refresh_token")
        }
    }
