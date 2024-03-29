# generated by datamodel-codegen:
#   filename:  task_created_event_schema.json
#   timestamp: 2022-05-19T12:02:33+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class EventTitleTaskCreated(Enum):
    TASK_CREATED = "TASK.CREATED"


class TaskStatus(Enum):
    OPEN = "OPEN"
    DONE = "DONE"


class UserInfoSchema(BaseModel):
    public_id: str = Field(..., title="Public Id")


class TaskDataSchema(BaseModel):
    public_id: str = Field(..., title="Public Id")
    title: str = Field(..., title="Title")
    description: str = Field(..., title="Description")
    status: TaskStatus
    assignee: Optional[UserInfoSchema] = None
    jira_id: Optional[int] = Field(None, title="Jira Id")


class TaskProducer(Enum):
    POPUG_TASKKEEPER = "POPUG_TASKKEEPER"


class TaskCreatedEventSchema(BaseModel):
    version: Optional[int] = Field(1, title="Version")
    produced_at: Optional[datetime] = Field(None, title="Produced At")
    title: Optional[EventTitleTaskCreated] = "TASK.CREATED"
    data: TaskDataSchema
    producer: Optional[TaskProducer] = "POPUG_TASKKEEPER"
