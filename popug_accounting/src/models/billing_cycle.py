from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    Table,
    text,
)
from utils import get_public_id

from popug_schema_registry.models.v1.billing_cycle_started_event_schema import (  # noqa: E501
    BillingCycleStatus,
)
from popug_sdk.db import mapper_registry


@mapper_registry.mapped
@dataclass
class BillingCycle:
    __table__ = Table(
        "billing_cycles",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "public_id",
            String(50),
            unique=True,
            default=get_public_id,
            nullable=False,
        ),
        Column(
            "status",
            Enum(BillingCycleStatus),
            nullable=False,
            default=BillingCycleStatus.ACTIVE,
            server_default=text(f"'{BillingCycleStatus.ACTIVE.value}'"),
        ),
        Column(
            "started_at",
            DateTime,
            nullable=False,
            default=datetime.utcnow,
            server_default=text("(now() at time zone 'utc')"),
        ),
        Column("processed_at", DateTime),
        Column("closed_at", DateTime),
    )

    id: int = field(init=False)
    public_id: str = field(default_factory=get_public_id)
    status: BillingCycleStatus = BillingCycleStatus.ACTIVE
    started_at: datetime = field(default_factory=datetime.utcnow)
    processed_at: datetime | None = None
    closed_at: datetime | None = None
