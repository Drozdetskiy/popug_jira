import enum
import uuid
from typing import Any

from constants import ROLES_SCOPE_MAP

from popug_schema_registry.models.v1.task_created_event_schema import UserRoles


def get_public_id() -> str:
    return uuid.uuid4().hex


def get_scopes(role: UserRoles) -> list[str]:
    return ROLES_SCOPE_MAP.get(role, [])


def dict_factory(data: list[tuple[str, Any]]) -> dict[str, Any]:
    return {
        key: value.value if isinstance(value, enum.Enum) else value
        for key, value in data
        if value is not None
    }
