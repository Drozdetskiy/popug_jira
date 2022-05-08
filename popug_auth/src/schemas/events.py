from dataclasses import dataclass
from datetime import datetime
from typing import Any

from constants import (
    Entities,
    EventTitles,
    EventTypes,
    UserRoles,
)
from pydantic import (
    BaseModel,
    Field,
)
from pydantic.dataclasses import dataclass as pydantic_dataclass
from utils import get_pid


@pydantic_dataclass
@dataclass
class UserSimpleData:
    pid: str
    username: str
    email: str
    role: UserRoles


@pydantic_dataclass
@dataclass
class UserRoleChangedData:
    pid: str
    role: UserRoles


class EventLogDataSchema(BaseModel):
    old_data: dict[str, Any] = Field(default_factory=dict)
    new_data: dict[str, Any] = Field(default_factory=dict)


class EventLogInitSchema(BaseModel):
    pid: str = Field(default_factory=get_pid)
    type: EventTypes = EventTypes.DATA_STREAMING
    entity: Entities = Field(default=Entities.USER)
    version: int = Field(1, gt=0)
    data: EventLogDataSchema = Field(default_factory=EventLogDataSchema)


class EventLogUserAddedInitSchema(EventLogInitSchema):
    title: EventTitles = EventTitles.ADDED
    type: EventTypes = EventTypes.BUSINESS_CALL


class EventLogUserRoleChangedInitSchema(EventLogInitSchema):
    title: EventTitles = EventTitles.ROLE_CHANGED
    type: EventTypes = EventTypes.BUSINESS_CALL


class EventLogUserDeletedInitSchema(EventLogInitSchema):
    title: EventTitles = EventTitles.DELETED


class EventLogSchema(BaseModel):
    title: EventTitles
    id: int
    pid: str
    entity: Entities
    type: EventTypes
    version: int
    data: EventLogDataSchema
    processed: bool
    created_at: datetime
    updated_at: datetime
