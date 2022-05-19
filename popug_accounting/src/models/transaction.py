from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
    field,
)
from datetime import datetime

from dto.task import TaskDTO
from dto.transaction import TransactionDTO
from dto.user import UserDTO
from models import (
    Task,
    User,
)
from models.billing_cycle import BillingCycle
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    text,
)
from sqlalchemy.orm import relationship
from utils import get_public_id

from popug_schema_registry.models.v1.transaction_added_event_schema import (
    TransactionTypes,
)
from popug_sdk.db import mapper_registry


@mapper_registry.mapped
@dataclass
class Transaction:
    __table__ = Table(
        "transactions",
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
            "debit",
            Integer,
            nullable=False,
            default=0,
            server_default=text("0"),
        ),
        Column(
            "credit",
            Integer,
            nullable=False,
            default=0,
            server_default=text("0"),
        ),
        Column("user_id", ForeignKey("users.id"), nullable=False),
        Column("task_id", ForeignKey("tasks.id")),
        Column(
            "billing_cycle_id", ForeignKey("billing_cycles.id"), nullable=False
        ),
        Column(
            "type",
            Enum(TransactionTypes),
            nullable=False,
            default=TransactionTypes.INCOME,
            server_default=text(f"'{TransactionTypes.INCOME.value}'"),
        ),
        Column(
            "created_at",
            DateTime,
            nullable=False,
            default=datetime.utcnow,
            server_default=text("(now() at time zone 'utc')"),
        ),
    )

    user_id: int
    billing_cycle_id: int
    debit: int = 0
    credit: int = 0
    id: int = field(init=False)
    task_id: int | None = None
    type: TransactionTypes = TransactionTypes.INCOME
    public_id: str = field(default_factory=get_public_id)
    created_at: datetime = field(default_factory=datetime.utcnow)
    task: Task | None = field(init=False)
    user: User = field(init=False)

    __mapper_args__ = {  # type: ignore
        "properties": {
            "user": relationship("User"),
            "task": relationship("Task"),
            "billing_cycle": relationship("BillingCycle"),
        },
    }

    @property
    def billing_cycle(self) -> BillingCycle:
        raise NotImplementedError

    def to_dto(self) -> TransactionDTO:
        data = asdict(self)
        data["user"] = UserDTO(**data["user"])

        task = data["task"]

        if task:
            data["task"] = TaskDTO.get_dto_from_dict(**task)

        return TransactionDTO(**data)
