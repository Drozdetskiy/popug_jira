from constants import UserRoles
from pydantic import BaseModel


class UserInfoSchema(BaseModel):
    id: int
    public_id: str
    username: str = ""
    role: UserRoles | None
