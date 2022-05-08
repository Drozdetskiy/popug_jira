from dataclasses import asdict
from typing import Any

from constants import UserEvents
from schemas.events import (
    EventLogDataSchema,
    EventLogInitSchema,
    EventLogUserAddedInitSchema,
    EventLogUserDeletedInitSchema,
    EventLogUserRoleChangedInitSchema,
    UserRoleChangedData,
    UserSimpleData,
)
from utils import dict_factory


def _create_user_added_event(
    old_user_data: dict[str, Any],
    new_user_data: dict[str, Any],
) -> EventLogUserAddedInitSchema:
    if old_user_data:
        raise ValueError("old_user_data shouldn`t exist for user_added event")

    new_data = UserSimpleData(
        pid=new_user_data["pid"],
        username=new_user_data["username"],
        email=new_user_data["email"],
        role=new_user_data["role"],
    )

    return EventLogUserAddedInitSchema(
        data=EventLogDataSchema(
            new_data=asdict(new_data, dict_factory=dict_factory),
        )
    )


def _create_user_role_changed_event(
    old_user_data: dict[str, Any],
    new_user_data: dict[str, Any],
) -> EventLogUserRoleChangedInitSchema:
    new_data = UserRoleChangedData(
        pid=new_user_data["pid"],
        role=new_user_data["role"],
    )
    old_data = UserRoleChangedData(
        pid=old_user_data["pid"],
        role=old_user_data["role"],
    )

    return EventLogUserRoleChangedInitSchema(
        data=EventLogDataSchema(
            old_data=asdict(old_data, dict_factory=dict_factory),
            new_data=asdict(new_data, dict_factory=dict_factory),
        )
    )


def _create_user_deleted_event(
    old_user_data: dict[str, Any],
    new_user_data: dict[str, Any],
) -> EventLogUserDeletedInitSchema:
    if new_user_data:
        raise ValueError(
            "new_user_data shouldn`t exist for user_deleted event"
        )

    old_data = UserSimpleData(
        pid=old_user_data["pid"],
        username=old_user_data["username"],
        email=old_user_data["email"],
        role=old_user_data["role"],
    )

    return EventLogUserDeletedInitSchema(
        data=EventLogDataSchema(
            old_data=asdict(old_data, dict_factory=dict_factory),
        )
    )


FABRIC_MAP = {
    UserEvents.USER_ADDED: _create_user_added_event,
    UserEvents.USER_ROLE_CHANGED: _create_user_role_changed_event,
    UserEvents.USER_DELETED: _create_user_deleted_event,
}


def event_fabric(
    event_title: UserEvents,
    old_user_data: dict[str, Any] | None = None,
    new_user_data: dict[str, Any] | None = None,
) -> EventLogInitSchema:
    return FABRIC_MAP[event_title](old_user_data or {}, new_user_data or {})
