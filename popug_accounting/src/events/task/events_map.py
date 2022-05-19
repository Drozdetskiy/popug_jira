from popug_schema_registry.models.v1.task_assigned_event_schema import (
    TaskAssignedEventSchema,
)
from popug_schema_registry.models.v1.task_completed_event_schema import (
    TaskCompletedEventSchema,
)
from popug_schema_registry.models.v1.task_created_event_schema import (
    TaskCreatedEventSchema,
)

TASK_EVENTS_MAP = {
    ("TASK.CREATED", 1): TaskCreatedEventSchema,
    ("TASK.ASSIGNED", 1): TaskAssignedEventSchema,
    ("TASK.COMPLETED", 1): TaskCompletedEventSchema,
}
