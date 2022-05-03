from dataclasses import dataclass

from constants import UserRoles


@dataclass
class UserDTO:
    id: int
    username: str
    role: UserRoles
    public_id: str
    is_deleted: bool
