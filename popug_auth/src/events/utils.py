from constants import EventTitles

ROUTING_KEY_TEMPLATE = "{event_title}.{version}"


def get_routing_key(title: EventTitles, version: int) -> str:
    return ROUTING_KEY_TEMPLATE.format(
        event_title=title.value.lower(),
        version=version,
    )
