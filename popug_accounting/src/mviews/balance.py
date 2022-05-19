from __future__ import annotations

from dataclasses import dataclass

from models import Transaction
from mviews.materialized_view import create_materialized_view
from sqlalchemy import (
    func,
    select,
)

from popug_sdk.db import mapper_registry

balance_query = select(
    func.sum(Transaction.debit).label("debit"),
    func.sum(Transaction.credit).label("credit"),
    Transaction.user_id,
    Transaction.billing_cycle_id,
).group_by(Transaction.user_id, Transaction.billing_cycle_id)


@mapper_registry.mapped
@dataclass
class Balance:
    __table__ = create_materialized_view(
        "balances",
        balance_query,
        primary_keys=(Transaction.user_id, Transaction.billing_cycle_id),
    )

    debit: int
    credit: int
    user_id: int
    billing_cycle_id: int
