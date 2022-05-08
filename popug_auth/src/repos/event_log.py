from __future__ import annotations

from models import EventLog
from schemas.events import EventLogInitSchema

from popug_sdk.repos.base import BaseRepo


class UserEventLogRepo(BaseRepo[EventLog]):
    def add_log(self, data: EventLogInitSchema) -> UserEventLogRepo:
        event_log = EventLog(**data.dict())
        self._session.add(event_log)

        return self(event_log)
