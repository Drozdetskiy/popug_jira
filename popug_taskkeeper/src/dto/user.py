from dataclasses import dataclass

from popug_schema_registry.models.v1.task_created_event_schema import UserRoles


@dataclass
class UserDTO:
    id: int
    username: str
    role: UserRoles
    public_id: str
    is_deleted: bool
