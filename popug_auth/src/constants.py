import enum


# TODO: Move to client library
@enum.unique
class UserRoles(enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"


@enum.unique
class Permissions(enum.Enum):
    CAN_READ_USERS = "CAN_READ_USERS"
    CAN_UPDATE_USER = "CAN_UPDATE_USER"
    CAN_READ_SELF_TASKS = "CAN_READ_SELF_TASKS"
    CAN_READ_ALL_TASKS = "CAN_READ_ALL_TASKS"
    CAN_ASSIGN_NEW_TASKS = "CAN_ASSIGN_NEW_TASKS"
    CAN_UPDATE_SELF_TASKS = "CAN_UPDATE_SELF_TASK"


# TODO: update scopes
ROLES_SCOPE_MAP = {
    UserRoles.EMPLOYEE: [
        Permissions.CAN_READ_USERS.value,
        Permissions.CAN_READ_SELF_TASKS.value,
        Permissions.CAN_READ_ALL_TASKS.value,
        Permissions.CAN_UPDATE_SELF_TASKS.value,
    ],
    UserRoles.ADMIN: [
        Permissions.CAN_READ_USERS.value,
        Permissions.CAN_UPDATE_USER.value,
        Permissions.CAN_READ_SELF_TASKS.value,
        Permissions.CAN_READ_ALL_TASKS.value,
        Permissions.CAN_UPDATE_SELF_TASKS.value,
        Permissions.CAN_ASSIGN_NEW_TASKS.value,
    ],
    UserRoles.MANAGER: [
        Permissions.CAN_READ_USERS.value,
        Permissions.CAN_UPDATE_USER.value,
        Permissions.CAN_READ_SELF_TASKS.value,
        Permissions.CAN_READ_ALL_TASKS.value,
        Permissions.CAN_UPDATE_SELF_TASKS.value,
        Permissions.CAN_ASSIGN_NEW_TASKS.value,
    ],
}


USER_AUTH_CODE_TEMPLATE = "user.auth_code.%s"


@enum.unique
class EventTitles(enum.Enum):
    USER_CREATED = "USER.CREATED"
    USER_ROLE_CHANGED = "USER.ROLE_CHANGED"
    USER_DELETED = "USER.DELETED"


@enum.unique
class EventTypes(enum.Enum):
    BUSINESS_CALL = "BUSINESS_CALL"
    DATA_STREAMING = "DATA_STREAMING"
