from __future__ import annotations

from typing import Any

from constants import TaskStatus
from models import (
    Task,
    User,
)

from popug_sdk.repos.base import BaseRepo


class TaskRepo(BaseRepo[Task]):
    def get_by_id(self, id_: int, lock: bool = False, **lock_params: Any):
        query = self._session.query(Task).outerjoin(User)

        if lock:
            query = query.with_for_update(**lock_params)

        return self(query.filter(Task.id == id_).first())

    def get_by_public_id(
        self, public_id: str, lock: bool = False, **lock_params: Any
    ) -> TaskRepo:
        query = self._session.query(Task, User)

        if lock:
            query = query.with_for_update(**lock_params)

        return self(query.filter(Task.public_id == public_id).first())

    def complete(self) -> TaskRepo:
        task = self.get()

        task.status = TaskStatus.DONE
        self._session.add(task)

        return self(task)

    def create_task(self, **data: dict[str, Any]) -> TaskRepo:
        task = Task(**data)

        self._session.add(task)

        return self(task)

    def assign_to_user(self, user_id: int) -> TaskRepo:
        task = self.get()
        task.assignee_id = user_id

        self._session.add(task)

        return self(task)


class TasksListRepo(BaseRepo[list[Task]]):
    def get_list(
        self, limit: int, offset: int, assignee_id: int | None = None
    ) -> TasksListRepo:
        query = self._session.query(Task).outerjoin(User)

        if assignee_id is not None:
            query = query.filter(Task.assignee_id == assignee_id)

        return self(query.order_by(User.id).offset(offset).limit(limit).all())

    def count_all(self, assignee_id: int | None) -> int:
        query = self._session.query(Task)

        if assignee_id is not None:
            query = query.filter(Task.assignee_id == assignee_id)

        return query.count()

    def get_all_opened(self) -> TasksListRepo:
        # TODO: add iterator
        return self(
            self._session.query(Task)
            .filter(Task.status == TaskStatus.OPEN)
            .all()
        )
