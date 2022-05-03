import json
import logging
from functools import singledispatch

from events.user.fabric import event_data_fabric
from repos.user import UserRepo
from schemas.events import (
    BaseEventSchema,
    UserCreatedEventSchema,
    UserDeletedEventSchema,
    UserRoleChangedEventSchema,
)

from popug_sdk.conf import settings
from popug_sdk.db import create_session

logger = logging.getLogger(settings.project)


@singledispatch
def _process_event(event: BaseEventSchema) -> None:
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
            .get()
        )
        logger.info(f"{user = } role changed")


@_process_event.register
def _create_user(event: UserCreatedEventSchema) -> None:
    with create_session() as session:
        data = event.data.dict()
        public_id = data.pop("public_id")
        user = UserRepo(session).create_or_update(public_id, **data).get()
        logger.info(f"{user = } user created")


def process_user_event_message(message: bytes) -> None:
    event = event_data_fabric(json.loads(message))
    logger.info(f"Processing event: {event}")
    _process_event(event)
