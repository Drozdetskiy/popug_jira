from __future__ import annotations

from mviews import Balance

from popug_sdk.repos.base import BaseRepo


class BalanceListRepo(BaseRepo[list[Balance]]):
    def get_list(
        self,
        billing_cycle_id: int,
        limit: int,
        offset: int,
        user_id: int | None = None,
    ) -> BalanceListRepo:
        query = self._session.query(Balance).filter(
            Balance.billing_cycle_id == billing_cycle_id
        )

        if user_id is not None:
            query = query.filter(Balance.user_id == user_id)

        return self(
            query.order_by(Balance.billing_cycle_id)
            .limit(limit)
            .offset(offset)
            .all()
        )

    def count_all(
        self,
        billing_cycle_id: int,
        user_id: int | None = None,
    ) -> int:
        query = self._session.query(Balance).filter(
            Balance.billing_cycle_id == billing_cycle_id
        )

        if user_id is not None:
            query = query.filter(Balance.user_id == user_id)

        return query.count()
