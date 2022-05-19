from __future__ import annotations

from typing import Any

from models import User

from popug_schema_registry.models.v1.task_created_event_schema import UserRoles
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

    def get_by_public_id(self, public_id: str) -> UserRepo:
        return self(
            self._session.query(User)
            .filter(User.public_id == public_id)
            .first()
        )

    def add(self, **data: Any) -> UserRepo:
        user = User(**data)
        self._session.add(user)

        return self(user)

    def change_role(self, role: UserRoles) -> UserRepo:
        user = self.get()
        user.role = role
        self._session.add(user)

        return self(user)

    def delete(self) -> UserRepo:
        user = self.get()
        self._session.delete(user)

        return self(user)


class UsersListRepo(BaseRepo[list[User]]):
    def count_all(self) -> int:
        return self._session.query(User).count()

    def get_list(self, limit: int, offset: int) -> UsersListRepo:
        return self(
            self._session.query(User)
            .order_by(User.id)
            .offset(offset)
            .limit(limit)
            .all()
        )
