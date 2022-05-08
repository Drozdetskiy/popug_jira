import json
from typing import Any

from constants import UserRoles
from pydantic import BaseModel


class UserInfoSimpleSchema(BaseModel):
    pid: str
    username: str
    email: str
    role: UserRoles

    # TODO: Fix this
    def dict(self, *args: Any, **kwargs: Any) -> Any:
        return json.loads(self.json(*args, **kwargs))


class UserInfoSchema(UserInfoSimpleSchema):
    id: int
    pid: str
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


class UserPIDSchema(BaseModel):
    pid: str
