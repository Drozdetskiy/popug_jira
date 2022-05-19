from datetime import datetime

from pydantic import BaseModel

from popug_schema_registry.models.v1.billing_cycle_started_event_schema import (  # noqa: E501
    BillingCycleStatus,
)


class BillingCycleSchema(BaseModel):
    id: int
    public_id: str
    status: BillingCycleStatus
    started_at: datetime
    processed_at: datetime | None = None
    closed_at: datetime | None = None
