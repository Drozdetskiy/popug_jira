from datetime import datetime

from constants import TaskStatus
from pydantic import BaseModel
from schemas.user import UserInfoSchema


class TaskSchema(BaseModel):
    id: int
    public_id: str
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    assignee: UserInfoSchema | None


class NewTaskSchema(BaseModel):
    title: str
    description: str


class ReshuffledIdsSchema(BaseModel):
    ids: list[int]
