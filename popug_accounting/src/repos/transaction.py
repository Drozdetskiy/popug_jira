from __future__ import annotations

from typing import Any

from models import Transaction
from sqlalchemy import func

from popug_sdk.repos.base import BaseRepo


class TransactionRepo(BaseRepo[Transaction]):
    def get_by_id(
        self, id_: int, lock: bool = False, **lock_params: Any
    ) -> TransactionRepo:
        query = self._session.query(Transaction)

        if lock:
            query = query.with_for_update(**lock_params)

        transaction = query.filter(Transaction.id == id_).first()

        return self(transaction)

    def add(self, **data: Any) -> TransactionRepo:
        transaction = Transaction(**data)
        self._session.add(transaction)

        return self(transaction)


class TransactionsListRepo(BaseRepo[list[Transaction]]):
    def get_by_billing_cycle_id(
        self, billing_cycle_id: int
    ) -> TransactionsListRepo:
        transactions = (
            self._session.query(Transaction)
            .filter(Transaction.billing_cycle_id == billing_cycle_id)
            .all()
        )

        return self(transactions)

    def get_all_users_in_cycle(
        self, billing_cycle_id: int
    ) -> list[tuple[int]]:
        user_ids = (
            self._session.query(Transaction.user_id)
            .filter(Transaction.billing_cycle_id == billing_cycle_id)
            .distinct(Transaction.user_id)
            .all()
        )

        return user_ids

    def get_balance_for_user_by_cycle(
        self, user_id: int, billing_cycle_id: int
    ) -> tuple[int, int]:
        result = (
            self._session.query(
                func.sum(Transaction.debit).label("debit"),
                func.sum(Transaction.credit).label("credit"),
            )
            .filter(
                Transaction.billing_cycle_id == billing_cycle_id,
                Transaction.user_id == user_id,
            )
            .all()
        )

        if result:
            return result[0]["debit"], result[0]["credit"]

        return 0, 0
