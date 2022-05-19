from enum import Enum

ROUTING_KEY_TEMPLATE = "{event_title}.{version}"


def get_routing_key(title: str | Enum, version: int) -> str:
    return ROUTING_KEY_TEMPLATE.format(
        event_title=title.value.lower()
        if isinstance(title, Enum)
        else title.lower(),
        version=version,
    )
