from dataclasses import dataclass
from datetime import datetime

from dto.task import TaskDTO
from dto.user import UserDTO

from popug_schema_registry.models.v1.transaction_added_event_schema import (
    TransactionTypes,
)


@dataclass
class TransactionDTO:
    id: int
    public_id: str
    debit: int
    credit: int
    user_id: int
    billing_cycle_id: int
    type: TransactionTypes
    user: UserDTO
    created_at: datetime
    task: TaskDTO | None = None
    task_id: int | None = None
