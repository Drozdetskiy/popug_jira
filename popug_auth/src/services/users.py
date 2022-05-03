from dataclasses import asdict

from constants import (
    EventTypes,
    UserRoles,
)
from events.user.producers import get_producer
from events.utils import get_routing_key
from models import User
from repos.user import (
    UserRepo,
    UsersListRepo,
)
from schemas.events import (
    UserCreatedEventSchema,
    UserDeletedEventSchema,
    UserRoleChangedEventSchema,
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
        return UsersListRepo(session).get_list(limit, offset).get()


def count_users() -> int:
    with create_session() as session:
        return UsersListRepo(session).count_all()


def get_user(user_id: int) -> User:
    with create_session() as session:
        try:
            user = UserRepo(session).get_by_id(user_id).get()
        except NoContextError:
            raise UserNotFound(f"User with id {user_id} not found")

        return user


def create_user(data: UserAddSchema) -> User:
    with create_session() as session:
        try:
            user = UserRepo(session).add(**data.dict()).apply()
        except IntegrityError:
            raise UserAlreadyExists

    event = UserCreatedEventSchema(data=asdict(user))
    producer = get_producer(EventTypes.DATA_STREAMING)
    producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),
    )

    return user


def change_user_role(user_id: int, role: UserRoles) -> User:
    with create_session() as session:
        user_repo = UserRepo(session)

        try:
            user = user_repo.get_by_id(user_id, lock=True).get()
        except NoContextError:
            raise UserNotFound(f"User with id {user_id} not found")

        old_role = user.role
        user_repo.change_role(role=role).apply()

    event = UserRoleChangedEventSchema(
        data={
            "public_id": user.public_id,
            "old_role": old_role,
            "new_role": role,
        }
    )
    producer = get_producer(EventTypes.BUSINESS_CALL)
    producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),
    )

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

    event = UserDeletedEventSchema(data=asdict(user))
    producer = get_producer(EventTypes.DATA_STREAMING)
    producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),
    )

    return user
