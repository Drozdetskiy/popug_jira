from __future__ import annotations

import enum
from typing import Any

from models import User
from repos.exceptions import InvalidUserDataError
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

from popug_schema_registry.models.v1.task_created_event_schema import UserRoles
from popug_sdk.repos.base import BaseRepo


class UserRepo(BaseRepo[User]):
    def get_by_id(
        self, id_: int, lock: bool = False, **lock_params: Any
    ) -> UserRepo:
        query = self._session.query(User)

        if lock:
            query = query.with_for_update(**lock_params)

        return self(query.filter(User.id == id_).first())

    def get_by_public_id(
        self, public_id: str, lock: bool = False, **lock_params: Any
    ) -> UserRepo:
        query = self._session.query(User)

        if lock:
            query = query.with_for_update(**lock_params)

        return self(query.filter(User.public_id == public_id).first())

    def create_or_update(self, public_id: str, **data: Any) -> UserRepo:
        user = self.get_by_public_id(public_id, lock=True).context()

        if not user:
            self._session.execute(
                insert(User)
                .values(public_id=public_id)
                .on_conflict_do_nothing(
                    index_elements=["public_id"],
                )
            )
            user = self.get_by_public_id(public_id, lock=True).get()

        if not user.is_deleted:
            for key, value in data.items():
                if key in User.get_updatable_fields():
                    old_value = getattr(user, key)

                    if isinstance(old_value, enum.Enum):
                        old_value = old_value.value

                    if isinstance(value, enum.Enum):
                        value = value.value

                    if old_value != value:
                        setattr(user, key, value)

            self._session.add(user)

        return self(user)

    def mark_as_deleted(self, public_id: str) -> UserRepo:
        user = self.get_by_public_id(public_id, lock=True).context()

        if not user:
            user = self.create_or_update(public_id, is_deleted=True).context()
        else:
            user.is_deleted = True
            self._session.add(user)

        return self(user)

    def delete(self) -> UserRepo:
        user = self.context()

        if user and user.is_deleted:
            self._session.delete(user)
        else:
            raise InvalidUserDataError(f"User {user} can`t be deleted")

        return self(user)


class UsersListRepo(BaseRepo[list[User]]):
    def get_random_employees(
        self, count: int = 1, lock: bool = False, **lock_params: Any
    ) -> UsersListRepo:
        query = self._session.query(User)

        if lock:
            query = query.with_for_update(**lock_params)

        return self(
            query.filter(
                User.role == UserRoles.EMPLOYEE,
                User.is_deleted.is_(False),  # type: ignore
            )
            .order_by(func.random())
            .limit(count)
        )

    def get_list(self, limit: int, offset: int) -> UsersListRepo:
        return self(
            self._session.query(User)
            .order_by(User.id)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def count_all(self) -> int:
        return self._session.query(User).count()
