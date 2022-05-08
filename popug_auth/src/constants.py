import enum


@enum.unique
class UserRoles(enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"


@enum.unique
class Permissions(enum.Enum):
    CAN_READ_USERS = "CAN_READ_USERS"
    CAN_UPDATE_USER = "CAN_UPDATE_USER"


# TODO: update scopes
ROLES_SCOPE_MAP = {
    UserRoles.EMPLOYEE: [
        Permissions.CAN_READ_USERS.value,
    ],
    UserRoles.ADMIN: [
        Permissions.CAN_READ_USERS.value,
        Permissions.CAN_UPDATE_USER.value,
    ],
    UserRoles.MANAGER: [
        Permissions.CAN_READ_USERS.value,
        Permissions.CAN_UPDATE_USER.value,
    ],
}


USER_AUTH_CODE_TEMPLATE = "user.auth_code.%s"


@enum.unique
class Entities(enum.Enum):
    USER = "USER"


@enum.unique
class EventTitles(enum.Enum):
    ADDED = "ADDED"
    ROLE_CHANGED = "ROLE_CHANGED"
    DELETED = "DELETED"


@enum.unique
class EventTypes(enum.Enum):
    BUSINESS_CALL = "BUSINESS_CALL"
    DATA_STREAMING = "DATA_STREAMING"


@enum.unique
class UserEvents(enum.Enum):
    USER_ADDED = "USER_ADDED"
    USER_ROLE_CHANGED = "USER_ROLE_CHANGED"
    USER_DELETED = "USER_DELETED"
