from constants import UserRoles
from models import User
from repos.user import (
    UserRepo,
    UsersRepo,
)
from schemas.user import UserAddSchema
from services.exceptions import (
    UserAlreadyExists,
    UserNotFound,
)
from sqlalchemy.exc import IntegrityError

from popug_sdk.db import create_session
from popug_sdk.repos.base import NoContextError


def get_users(limit: int, offset: int) -> list[User]:
    with create_session() as session:
        return UsersRepo(session).get_list(limit, offset).get()


def count_users() -> int:
    with create_session() as session:
        return UsersRepo(session).count_all()


def get_user(user_id: int) -> User:
    with create_session() as session:
        try:
            user = UserRepo(session).get_by_id(user_id).get()
        except NoContextError:
            raise UserNotFound(f"User with id {user_id} not found")

        return user


def add_user(data: UserAddSchema) -> User:
    with create_session() as session:
        try:
            user = UserRepo(session).add(**data.dict()).apply()
        except IntegrityError:
            raise UserAlreadyExists

        return user


def change_user_role(user_id: int, role: UserRoles) -> User:
    with create_session() as session:
        try:
            user = (
                UserRepo(session)
                .get_by_id(user_id, lock=True)
                .change_role(role=role)
                .apply()
            )
        except NoContextError:
            raise UserNotFound(f"User with id {user_id} not found")

        return user


def delete_user(user_id: int) -> User:
    with create_session() as session:
        try:
            user = (
                UserRepo(session)
                .get_by_id(user_id, lock=True)
                .delete()
                .apply()
            )
        except NoContextError:
            raise UserNotFound(f"User with id {user_id} not found")

        return user
