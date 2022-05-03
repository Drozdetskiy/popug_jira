import enum


class UserRoles(enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"


# TODO: update scopes
ROLES_SCOPE_MAP = {
    UserRoles.EMPLOYEE: ["can_read"],
    UserRoles.ADMIN: ["can_read"],
    UserRoles.MANAGER: ["can_read"],
}


USER_AUTH_CODE_TEMPLATE = "user.auth_code.%s"
