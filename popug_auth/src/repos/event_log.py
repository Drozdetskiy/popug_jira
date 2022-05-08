from __future__ import annotations

from functools import singledispatchmethod

from models import EventLog
from pydantic import BaseModel
from schemas.events import (
    EventLogCreateBaseSchema,
    EventLogUserAddedCreateSchema,
    EventLogUserDeletedCreateSchema,
    EventLogUserRoleChangedCreateSchema,
    EventLogUserRoleChangedDataSchema,
    UserAddedDataSchema,
    UserDeletedDataSchema,
)

from popug_sdk.repos.base import BaseRepo


class UserEventLogRepo(BaseRepo[EventLog]):
    def _create_event_log(self, data: EventLogCreateBaseSchema) -> None:
        event_log = EventLog(**data.dict())
        self._session.add(event_log)
        self._append_context(event_log)

    def log(self, data: BaseModel) -> UserEventLogRepo:
        self._log(data)

        return self

    @singledispatchmethod
    def _log(self, data: BaseModel) -> None:
        raise NotImplementedError

    @_log.register
    def _log_user_added(self, data: UserAddedDataSchema) -> None:
        self._create_event_log(EventLogUserAddedCreateSchema(data=data))

    @_log.register
    def _log_user_deleted(self, data: UserDeletedDataSchema) -> None:
        self._create_event_log(EventLogUserDeletedCreateSchema(data=data))

    @_log.register
    def _log_user_role_changed(
        self, data: EventLogUserRoleChangedDataSchema
    ) -> None:
        self._create_event_log(EventLogUserRoleChangedCreateSchema(data=data))
