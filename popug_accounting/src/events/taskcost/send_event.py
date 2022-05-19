from datetime import datetime

from constants import ProducerTypes
from events.producers import get_producer
from events.utils import get_routing_key
from models import (
    Task,
    TaskCost,
)

from popug_schema_registry.models.v1.task_cost_added_event_schema import (
    TaskCostAddedEventSchema,
)


def send_taskcost_added_event(taskcost: TaskCost, task: Task) -> None:
    producer = get_producer(ProducerTypes.TASKCOSTS_BC)
    event = TaskCostAddedEventSchema(
        data={
            "public_id": taskcost.public_id,
            "task_public_id": task.public_id,
            "debit_cost": taskcost.debit_cost,
            "credit_cost": taskcost.credit_cost,
        },
        produced_at=datetime.utcnow(),
    )
    producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),
    )
