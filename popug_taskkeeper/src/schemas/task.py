from datetime import datetime

from pydantic import BaseModel
from schemas.user import UserInfoSchema

from popug_schema_registry.models.v1.task_created_event_schema import (
    TaskStatus,
)


class TaskSchema(BaseModel):
    id: int
    public_id: str
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    assignee: UserInfoSchema | None
    jira_id: int | None


class NewTaskSchema(BaseModel):
    jira_id: int
    title: str
    description: str


class ReshuffledIdsSchema(BaseModel):
    ids: list[int]
