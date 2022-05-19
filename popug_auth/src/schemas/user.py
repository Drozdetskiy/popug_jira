from pydantic import BaseModel

from popug_schema_registry.models.v1.task_created_event_schema import UserRoles


class UserInfoSchema(BaseModel):
    id: int
    public_id: str
    username: str
    email: str
    role: UserRoles


class UserAddSchema(BaseModel):
    username: str
    email: str
    role: UserRoles = UserRoles.EMPLOYEE
    beak_shape: str


class UserUpdateSchema(BaseModel):
    role: UserRoles


class UserPublicIDSchema(BaseModel):
    public_id: str
