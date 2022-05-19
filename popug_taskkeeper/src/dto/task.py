from dataclasses import dataclass
from datetime import datetime

from dto.user import UserDTO

from popug_schema_registry.models.v1.task_created_event_schema import (
    TaskStatus,
)


@dataclass
class TaskDTO:
    id: int
    public_id: str
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    assignee_id: int
    assignee: UserDTO | None
