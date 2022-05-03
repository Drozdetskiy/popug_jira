from models import User
from repos.user import UserRepo
from services.exception import UserNotFound

from popug_sdk.db import create_session
from popug_sdk.repos.base import NoContextError


def get_user_by_public_id(public_id: str) -> User:
    with create_session() as session:
        try:
            user = UserRepo(session).get_by_public_id(public_id).get()
        except NoContextError:
            raise UserNotFound(f"User with public_id {public_id} not found")

        return user
