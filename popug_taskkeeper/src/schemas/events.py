from datetime import datetime

from constants import (
    EventTitles,
    TaskStatus,
    UserRoles,
)
from pydantic import (
    BaseModel,
    Field,
)
from schemas.user import UserInfoSchema

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


class TaskDataSchema(BaseModel):
    public_id: str
    title: str
    description: str
    status: TaskStatus
    assignee: UserInfoSchema | None


class TaskCreatedEventSchema(BaseEventSchema):
    title: EventTitles = EventTitles.TASK_CREATED
    data: TaskDataSchema


class TaskNewAssigneeDataSchema(BaseModel):
    public_id: str
    old_assignee_public_id: str | None
    new_assignee_public_id: str


class TaskAssignedEventSchema(BaseEventSchema):
    title: EventTitles = EventTitles.TASK_ASSIGNED
    data: TaskNewAssigneeDataSchema


class TaskStatusChangedDataSchema(BaseModel):
    public_id: str
    old_status: TaskStatus
    new_status: TaskStatus


class TaskCompletedEventSchema(BaseEventSchema):
    title: EventTitles = EventTitles.TASK_COMPLETED
    data: TaskStatusChangedDataSchema
