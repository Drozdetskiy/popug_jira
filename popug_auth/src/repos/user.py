from __future__ import annotations

from dataclasses import asdict
from typing import Any

from constants import (
    UserEvents,
    UserRoles,
)
from events.user.fabric import event_fabric
from models import User
from repos.event_log import UserEventLogRepo

from popug_sdk.repos.base import BaseRepo


class UserRepo(BaseRepo[User]):
    def get_by_beak_shape(self, beak_shape: str) -> UserRepo:
        return self(
            self._session.query(User)
            .filter(User.beak_shape == beak_shape)
            .first()
        )

    def get_by_id(
        self, user_id: int, lock: bool = False, **lock_params: Any
    ) -> UserRepo:
        query = self._session.query(User)

        if lock:
            query = query.with_for_update(**lock_params)

        return self(query.filter(User.id == user_id).first())

    def get_by_pid(self, pid: str) -> UserRepo:
        return self(self._session.query(User).filter(User.pid == pid).first())

    def add(self, **data: Any) -> UserRepo:
        user = User(**data)
        self._session.add(user)

        UserEventLogRepo(self._session).add_log(
            event_fabric(UserEvents.USER_ADDED, new_user_data=asdict(user))
        )

        return self(user)

    def change_role(self, role: UserRoles) -> UserRepo:
        user = self.get()
        old_user_data = asdict(user)

        user.role = role
        self._session.add(user)

        new_user_data = asdict(user)

        UserEventLogRepo(self._session).add_log(
            event_fabric(
                UserEvents.USER_ROLE_CHANGED,
                new_user_data=new_user_data,
                old_user_data=old_user_data,
            )
        )

        return self(user)

    def delete(self) -> UserRepo:
        user = self.get()
        old_user_data = asdict(user)
        self._session.delete(user)

        UserEventLogRepo(self._session).add_log(
            event_fabric(
                UserEvents.USER_DELETED,
                old_user_data=old_user_data,
            )
        )

        return self(user)


class UsersRepo(BaseRepo[list[User]]):
    def count_all(self) -> int:
        return self._session.query(User).count()

    def get_list(self, limit: int, offset: int) -> UsersRepo:
        return self(
            self._session.query(User)
            .order_by(User.id)
            .offset(offset)
            .limit(limit)
            .all()
        )
