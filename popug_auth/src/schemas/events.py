import json
from datetime import datetime
from typing import Any

from constants import (
    Entities,
    EventTypes,
    UserRoles,
)
from pydantic import (
    BaseModel,
    Field,
)
from schemas.user import UserInfoSimpleSchema
from utils import get_pid


class EventLogCreateBaseSchema(BaseModel):
    pid: str = Field(default_factory=get_pid)
    type: EventTypes
    entity: Entities = Field(default=Entities.USER)
    version: int = Field(1, gt=0)


class EventLogBaseSchema(BaseModel):
    type: EventTypes
    id: int
    pid: str
    entity: Entities
    version: int
    processed: bool
    next_retry_at: datetime | None
    retry_count: int
    created_at: datetime
    updated_at: datetime


class UserAddedDataSchema(BaseModel):
    old_data: dict[str, Any] = Field(default_factory=dict)
    new_data: UserInfoSimpleSchema


class EventLogUserAddedCreateSchema(EventLogCreateBaseSchema):
    type: EventTypes = EventTypes.ADDED
    data: UserAddedDataSchema


class EventLogUserAddedSchema(EventLogBaseSchema):
    data: UserAddedDataSchema


class UserRoleChangedDataSchema(BaseModel):
    pid: str
    role: UserRoles

    # TODO: Fix
    def dict(self, *args: Any, **kwargs: Any) -> Any:
        return json.loads(self.json(*args, **kwargs))


class EventLogUserRoleChangedDataSchema(BaseModel):
    old_data: UserRoleChangedDataSchema
    new_data: UserRoleChangedDataSchema


class EventLogUserRoleChangedCreateSchema(EventLogCreateBaseSchema):
    type: EventTypes = EventTypes.ROLE_CHANGED
    data: EventLogUserRoleChangedDataSchema


class EventLogUserRoleChangedSchema(EventLogBaseSchema):
    data: EventLogUserRoleChangedDataSchema


class UserDeletedDataSchema(BaseModel):
    old_data: UserInfoSimpleSchema
    new_data: dict[str, Any] = Field(default_factory=dict)


class EventLogUserDeletedCreateSchema(EventLogCreateBaseSchema):
    type: EventTypes = EventTypes.DELETED
    data: UserDeletedDataSchema


class EventLogUserDeletedSchema(EventLogBaseSchema):
    data: UserDeletedDataSchema
