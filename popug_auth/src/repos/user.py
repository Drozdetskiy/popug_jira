from models import User
from repos.base import BaseRepo


class UserRepo(BaseRepo):
    def get_by_beak_shape(self, beak_shape: str) -> User | None:
        return (
            self._session.query(User)
            .filter(User.beak_shape == beak_shape)
            .first()
        )

    def get_by_id(self, user_id: int) -> User | None:
        return self._session.query(User).filter(User.id == user_id).first()

    def get_by_pid(self, pid: str) -> User | None:
        return self._session.query(User).filter(User.pid == pid).first()
