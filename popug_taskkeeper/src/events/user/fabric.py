from typing import Any

from constants import EventTitles
from schemas.events import (
    BaseEventSchema,
    UserCreatedEventSchema,
    UserDeletedEventSchema,
    UserRoleChangedEventSchema,
)

USER_EVENTS_MAP = {
    (EventTitles.USER_CREATED, 1): UserCreatedEventSchema,
    (EventTitles.USER_ROLE_CHANGED, 1): UserRoleChangedEventSchema,
    (EventTitles.USER_DELETED, 1): UserDeletedEventSchema,
}


# TODO: Remove when schema registry will be added
def event_data_fabric(data: dict[str, Any]) -> BaseEventSchema:
    title = data.get("title")
    version = data.get("version")
    schema = USER_EVENTS_MAP.get((EventTitles(title), version))

    if not schema:
        raise ValueError(f"Unknown event: {data}")

    return schema(**data)
