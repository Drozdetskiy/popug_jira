from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

from logic import (
    get_credit_cost,
    get_debit_cost,
)
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from utils import get_public_id

from popug_sdk.db import mapper_registry


@mapper_registry.mapped
@dataclass
class TaskCost:
    __table__ = Table(
        "taskcosts",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "public_id",
            String(50),
            unique=True,
            nullable=False,
            default=get_public_id,
        ),
        Column("task_id", ForeignKey("tasks.id"), nullable=False, unique=True),
        Column(
            "credit_cost", Integer, nullable=False, default=get_credit_cost
        ),
        Column("debit_cost", Integer, nullable=False, default=get_debit_cost),
    )

    credit_cost: int = field(default_factory=get_credit_cost)
    debit_cost: int = field(default_factory=get_debit_cost)
    public_id: str = field(default_factory=get_public_id)
    id: int = field(init=False)
    task_id: int = field(init=False)
