from pydantic import BaseModel

from popug_schema_registry.models.v1.task_created_event_schema import UserRoles


class UserInfoSchema(BaseModel):
    id: int
    public_id: str
    username: str = ""
    role: UserRoles | None
