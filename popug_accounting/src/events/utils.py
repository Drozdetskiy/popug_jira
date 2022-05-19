from enum import Enum
from typing import (
    Any,
    Type,
)

from pydantic import BaseModel

ROUTING_KEY_TEMPLATE = "{event_title}.{version}"


def get_routing_key(title: str | Enum, version: int) -> str:
    return ROUTING_KEY_TEMPLATE.format(
        event_title=title.value.lower() if isinstance(title, Enum) else title,
        version=version,
    )


# TODO: Remove when schema registry will be added
def event_data_fabric(
    data: dict[str, Any],
    event_map: dict[tuple[str, int], Type[BaseModel]],
) -> BaseModel:
    title = data.get("title")
    version = data.get("version")
    schema = event_map.get((title, version))  # type: ignore

    if not schema:
        raise ValueError(f"Unknown event: {data}")

    return schema(**data)
