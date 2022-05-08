from __future__ import annotations

from typing import Any

from models import UserRefreshToken
from sqlalchemy.dialects.postgresql import insert

from popug_sdk.repos.base import BaseRepo


class UserRefreshTokenRepo(BaseRepo[UserRefreshToken]):
    def get_user_by_id(
        self, user_id: int, lock: bool = False, **lock_params: Any
    ) -> UserRefreshTokenRepo:
        query = self._session.query(UserRefreshToken)

        if lock:
            query = query.with_for_update(**lock_params)

        user_refresh_token: UserRefreshToken | None = query.filter(
            UserRefreshToken.user_id == user_id
        ).first()
        self._append_context(user_refresh_token)

        return self

    def upsert_refresh_token(
        self, user_id: int, refresh_token: str
    ) -> UserRefreshTokenRepo:
        if not self.is_empty:
            raise Exception("Cannot upsert refresh token while in context")

        self.get_user_by_id(user_id=user_id, lock=True)

        if self.is_empty:
            self._session.execute(
                insert(UserRefreshToken)
                .values(user_id=user_id, refresh_token=refresh_token)
                .on_conflict_do_update(
                    index_elements=["user_id"],
                    set_={"refresh_token": refresh_token},
                )
            )
            self.get_user_by_id(user_id=user_id, lock=True)
        else:
            user_refresh_token = self.get()
            user_refresh_token.refresh_token = refresh_token
            self._session.add(user_refresh_token)
            self._append_context(user_refresh_token)

        return self
