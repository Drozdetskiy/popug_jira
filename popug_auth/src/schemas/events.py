from datetime import datetime

from constants import (
    EventTitles,
    UserRoles,
)
from pydantic import (
    BaseModel,
    Field,
)

from popug_sdk.conf import settings


class BaseEventSchema(BaseModel):
    title: EventTitles
    version: int = 1
    producer: str = settings.project
    produced_at: datetime = Field(default_factory=datetime.utcnow)


class UserDataSchema(BaseModel):
    public_id: str
    username: str
    email: str
    role: UserRoles


class UserCreatedEventSchema(BaseEventSchema):
    title: EventTitles = EventTitles.USER_CREATED
    data: UserDataSchema


class UserDeletedEventSchema(BaseEventSchema):
    title: EventTitles = EventTitles.USER_DELETED
    data: UserDataSchema


class UserRoleChangedDataSchema(BaseModel):
    public_id: str
    old_role: UserRoles | None
    new_role: UserRoles


class UserRoleChangedEventSchema(BaseEventSchema):
    title: EventTitles = EventTitles.USER_ROLE_CHANGED
    data: UserRoleChangedDataSchema
