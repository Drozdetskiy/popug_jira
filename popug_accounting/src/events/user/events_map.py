from popug_schema_registry.models.v1.user_created_event_schema import (
    UserCreatedEventSchema,
)
from popug_schema_registry.models.v1.user_deleted_event_schema import (
    UserDeletedEventSchema,
)
from popug_schema_registry.models.v1.user_role_changed_event_schema import (
    UserRoleChangedEventSchema,
)

USER_EVENTS_MAP = {
    ("USER.CREATED", 1): UserCreatedEventSchema,
    ("USER.ROLE_CHANGED", 1): UserRoleChangedEventSchema,
    ("USER.DELETED", 1): UserDeletedEventSchema,
}
