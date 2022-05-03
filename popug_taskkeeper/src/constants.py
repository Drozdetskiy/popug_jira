import enum


# TODO: Move to auth client library
@enum.unique
class UserRoles(enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"


@enum.unique
class EventTitles(enum.Enum):
    USER_CREATED = "USER.CREATED"
    USER_ROLE_CHANGED = "USER.ROLE_CHANGED"
    USER_DELETED = "USER.DELETED"

    TASK_CREATED = "TASK.CREATED"
    TASK_ASSIGNED = "TASK.ASSIGNED"
    TASK_COMPLETED = "TASK.COMPLETED"


@enum.unique
class EventTypes(enum.Enum):
    BUSINESS_CALL = "BUSINESS_CALL"
    DATA_STREAMING = "DATA_STREAMING"


@enum.unique
class TaskStatus(enum.Enum):
    OPEN = "OPEN"
    DONE = "DONE"
