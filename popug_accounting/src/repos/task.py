from __future__ import annotations

import enum
from typing import Any

from models import Task
from sqlalchemy.dialects.postgresql import insert

from popug_sdk.repos.base import BaseRepo


class TaskRepo(BaseRepo[Task]):
    def get_by_id(
        self, id_: int, lock: bool = False, **lock_params: Any
    ) -> TaskRepo:
        query = self._session.query(Task)

        if lock:
            query = query.with_for_update(**lock_params)

        return self(query.filter(Task.id == id_).first())

    def get_by_public_id(
        self, public_id: str, lock: bool = False, **lock_params: Any
    ) -> TaskRepo:
        query = self._session.query(Task)

        if lock:
            query = query.with_for_update(**lock_params)

        return self(query.filter(Task.public_id == public_id).first())

    def create_or_update(self, public_id: str, **data: Any) -> TaskRepo:
        task = self.get_by_public_id(public_id, lock=True).context()

        if not task:
            self._session.execute(
                insert(Task)
                .values(public_id=public_id)
                .on_conflict_do_nothing(
                    index_elements=["public_id"],
                )
            )
            task = self.get_by_public_id(public_id, lock=True).get()

        for key, value in data.items():
            if key in Task.get_updatable_fields():
                old_value = getattr(task, key)

                if isinstance(old_value, enum.Enum):
                    old_value = old_value.value

                if isinstance(value, enum.Enum):
                    value = value.value

                if old_value != value:
                    setattr(task, key, value)

        self._session.add(task)

        return self(task)
