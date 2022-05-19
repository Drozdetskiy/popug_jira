from __future__ import annotations

from typing import Any

from logic import (
    get_credit_cost,
    get_debit_cost,
)
from models import TaskCost
from sqlalchemy.dialects.postgresql import insert

from popug_sdk.repos.base import BaseRepo


class TaskCostRepo(BaseRepo[TaskCost]):
    def get_by_task_id(
        self, task_id: int, lock: bool = False, **lock_params: Any
    ) -> TaskCostRepo:
        query = self._session.query(TaskCost)

        if lock:
            query = query.with_for_update(**lock_params)

        return self(query.filter(TaskCost.task_id == task_id).first())

    def add(self, task_id: int) -> TaskCostRepo:
        taskcost = self.context()

        if taskcost is None:
            self._session.execute(
                insert(TaskCost)
                .values(
                    credit_cost=get_credit_cost(),
                    debit_cost=get_debit_cost(),
                    task_id=task_id,
                )
                .on_conflict_do_nothing(
                    index_elements=["public_id"],
                )
            )

            taskcost = self.get_by_task_id(task_id).get()

        return self(taskcost)
