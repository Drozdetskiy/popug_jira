from __future__ import annotations

from dataclasses import asdict
from typing import Any

from constants import UserRoles
from models import User
from repos.event_log import UserEventLogRepo
from schemas.events import (
    EventLogUserRoleChangedDataSchema,
    UserAddedDataSchema,
    UserDeletedDataSchema,
)

from popug_sdk.repos.base import BaseRepo


class UserRepo(BaseRepo[User]):
    def get_by_beak_shape(self, beak_shape: str) -> UserRepo:
        self._append_context(
            self._session.query(User)
            .filter(User.beak_shape == beak_shape)
            .first()
        )

        return self

    def get_by_id(
        self, user_id: int, lock: bool = False, **lock_params: Any
    ) -> UserRepo:
        query = self._session.query(User)

        if lock:
            query = query.with_for_update(**lock_params)

        self._append_context(query.filter(User.id == user_id).first())

        return self

    def get_by_pid(self, pid: str) -> UserRepo:
        self._append_context(
            self._session.query(User).filter(User.pid == pid).first()
        )

        return self

    def add(self, **data: Any) -> UserRepo:
        user = User(**data)
        self._session.add(user)
        self._append_context(user)

        UserEventLogRepo(self._session).log(
            UserAddedDataSchema(new_data=asdict(user))
        )

        return self

    def change_role(self, role: UserRoles) -> UserRepo:
        user = self.get()
        old_user_data = asdict(user)
        user.role = role
        self._session.add(user)
        self._append_context(user)

        UserEventLogRepo(self._session).log(
            EventLogUserRoleChangedDataSchema(
                old_data=old_user_data, new_data=asdict(user)
            )
        )

        return self

    def delete(self) -> UserRepo:
        user = self.get()
        self._session.delete(user)
        self._append_context(user)

        UserEventLogRepo(self._session).log(
            UserDeletedDataSchema(old_data=asdict(user))
        )

        return self


class UsersRepo(BaseRepo[list[User]]):
    def count_all(self) -> int:
        return self._session.query(User).count()

    def get_list(self, limit: int, offset: int) -> UsersRepo:
        self._append_context(
            self._session.query(User)
            .order_by(User.id)
            .offset(offset)
            .limit(limit)
            .all()
        )

        return self
