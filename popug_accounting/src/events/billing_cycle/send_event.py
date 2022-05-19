from datetime import datetime
from typing import Type

from constants import ProducerTypes
from events.producers import get_producer
from events.utils import get_routing_key
from models import BillingCycle
from pydantic import BaseModel

from popug_schema_registry.models.v1.billing_cycle_closed_event_schema import (
    BillingCycleClosedEventSchema,
)
from popug_schema_registry.models.v1.billing_cycle_processed_event_schema import (  # noqa: E501
    BillingCycleProcessedEventSchema,
)
from popug_schema_registry.models.v1.billing_cycle_started_event_schema import (  # noqa: E501
    BillingCycleStartedEventSchema,
)


def _send_billing_cycle_event(
    event_schema: Type[BaseModel], billing_cycle: BillingCycle
) -> None:
    producer = get_producer(ProducerTypes.BILLING_CYCLES_BC)
    event = event_schema(
        data={
            "public_id": billing_cycle.public_id,
            "status": billing_cycle.status.value,
            "started_at": billing_cycle.started_at,
            "closed_at": billing_cycle.closed_at,
            "processed_at": billing_cycle.processed_at,
        },
        produced_at=datetime.utcnow(),
    )
    producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),  # type: ignore
    )


def send_billing_cycle_started_event(billing_cycle: BillingCycle) -> None:
    _send_billing_cycle_event(BillingCycleStartedEventSchema, billing_cycle)


def send_billing_cycle_closed_event(billing_cycle: BillingCycle) -> None:
    _send_billing_cycle_event(BillingCycleClosedEventSchema, billing_cycle)


def send_billing_cycle_processed_event(billing_cycle: BillingCycle) -> None:
    _send_billing_cycle_event(BillingCycleProcessedEventSchema, billing_cycle)
