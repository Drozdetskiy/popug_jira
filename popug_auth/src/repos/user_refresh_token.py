from models import UserRefreshToken
from repos.base import BaseRepo
from sqlalchemy.dialects.postgresql import insert


class UserRefreshTokenRepo(BaseRepo):
    def get_user_by_id(self, user_id: int) -> UserRefreshToken | None:
        return (
            self._session.query(UserRefreshToken)
            .filter(UserRefreshToken.user_id == user_id)
            .first()
        )

    def upsert(self, user_id: int, refresh_token: str) -> None:
        user_refresh_token = (
            self._session.query(UserRefreshToken)
            .with_for_update()
            .filter(UserRefreshToken.user_id == user_id)
            .first()
        )

        if user_refresh_token is None:
            self._session.execute(
                insert(UserRefreshToken)
                .values(user_id=user_id, refresh_token=refresh_token)
                .on_conflict_do_update(
                    index_elements=["user_id"],
                    set_={"refresh_token": refresh_token},
                )
            )
        else:
            user_refresh_token.refresh_token = refresh_token
            self._session.add(user_refresh_token)
