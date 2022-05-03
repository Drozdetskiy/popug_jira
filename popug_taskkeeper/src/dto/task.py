from dataclasses import dataclass
from datetime import datetime

from constants import TaskStatus
from dto.user import UserDTO


@dataclass
class TaskDTO:
    id: int
    public_id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    assignee_id: int
    assignee: UserDTO | None
