from constants import UserRoles
from pydantic import BaseModel


class UserInfoSchema(BaseModel):
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
