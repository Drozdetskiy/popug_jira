from __future__ import annotations

from datetime import datetime
from typing import Any

from models import BillingCycle
from repos.exceptions import NoActiveCycleError
from sqlalchemy import desc

from popug_schema_registry.models.v1.billing_cycle_started_event_schema import (  # noqa: E501
    BillingCycleStatus,
)
from popug_sdk.repos.base import BaseRepo


class BillingCycleRepo(BaseRepo[BillingCycle]):
    def get_last(
        self, lock: bool = False, **lock_params: Any
    ) -> BillingCycleRepo:
        query = self._session.query(BillingCycle)

        if lock:
            query = query.with_for_update(**lock_params)

        cycle = query.order_by(desc(BillingCycle.id)).first()

        if cycle and cycle.status != BillingCycleStatus.ACTIVE:
            raise NoActiveCycleError

        return self(cycle)

    def get_last_closed(
        self, lock: bool = False, **lock_params: Any
    ) -> BillingCycleRepo:
        query = self._session.query(BillingCycle)

        if lock:
            query = query.with_for_update(**lock_params)

        cycles = query.filter(
            BillingCycle.status == BillingCycleStatus.CLOSED
        ).all()

        if cycles:
            return self(cycles[0])

        return self(None)

    def create_active(self) -> BillingCycleRepo:
        cycle = BillingCycle()
        self._session.add(cycle)

        return self(cycle)

    def process(self) -> BillingCycleRepo:
        cycle = self.get()
        cycle.status = BillingCycleStatus.PROCESSED
        cycle.processed_at = datetime.utcnow()
        self._session.add(cycle)

        return self(cycle)

    def close(self) -> BillingCycleRepo:
        cycle = self.get()
        cycle.status = BillingCycleStatus.CLOSED
        cycle.closed_at = datetime.utcnow()
        self._session.add(cycle)

        return self(cycle)
