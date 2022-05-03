import enum
import uuid
from typing import Any


def get_public_id() -> str:
    return uuid.uuid4().hex


def dict_factory(data: list[tuple[str, Any]]) -> dict[str, Any]:
    return {
        key: value.value if isinstance(value, enum.Enum) else value
        for key, value in data
        if value is not None
    }
