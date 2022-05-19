import json
import logging
from functools import singledispatch

from events.user.events_map import USER_EVENTS_MAP
from events.utils import event_data_fabric
from pydantic import BaseModel
from repos.user import UserRepo

from popug_schema_registry.models.v1.user_created_event_schema import (
    UserCreatedEventSchema,
)
from popug_schema_registry.models.v1.user_deleted_event_schema import (
    UserDeletedEventSchema,
)
from popug_schema_registry.models.v1.user_role_changed_event_schema import (
    UserRoleChangedEventSchema,
)
from popug_sdk.conf import settings
from popug_sdk.db import create_session

logger = logging.getLogger(settings.project)


@singledispatch
def _process_event(event: BaseModel) -> None:
    raise NotImplementedError


@_process_event.register
def _delete_user(event: UserDeletedEventSchema) -> None:
    with create_session() as session:
        public_id = event.data.public_id
        user = UserRepo(session).mark_as_deleted(public_id).apply()
        logger.info(f"{user = } deleted")


@_process_event.register
def _change_user_role(event: UserRoleChangedEventSchema) -> None:
    with create_session() as session:
        user = (
            UserRepo(session)
            .create_or_update(event.data.public_id, role=event.data.new_role)
            .apply()
        )
        logger.info(f"{user = } role changed")


@_process_event.register
def _create_user(event: UserCreatedEventSchema) -> None:
    with create_session() as session:
        data = event.data.dict()
        public_id = data.pop("public_id")
        user = UserRepo(session).create_or_update(public_id, **data).apply()
        logger.info(f"{user = } user created")


def process_user_event_message(message: bytes) -> None:
    event = event_data_fabric(json.loads(message), USER_EVENTS_MAP)
    logger.info(f"Processing event: {event}")
    _process_event(event)
