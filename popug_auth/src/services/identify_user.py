from typing import TYPE_CHECKING

import jwt
from constants import USER_AUTH_CODE_TEMPLATE
from jwt import PyJWTError
from models import User
from repos.user import UserRepo
from services.exceptions import (
    AuthorizationCodeInvalid,
    InvalidTokenException,
    UserNotFound,
)

from popug_sdk.conf import settings
from popug_sdk.conf.auth import AuthSettings
from popug_sdk.db import create_session
from popug_sdk.repos.base import NoContextError

if TYPE_CHECKING:
    from redis import Redis as BaseRedis

    Redis = BaseRedis[str]
else:
    from redis import Redis


def identify_user_by_beak_shape(beak_shape: str) -> User:
    with create_session() as session:
        try:
            user = UserRepo(session).get_by_beak_shape(beak_shape).get()
        except NoContextError:
            raise UserNotFound(f"User with beak shape {beak_shape} not found")

    return user


def identify_user_by_auth_code(redis: Redis, code: str) -> User:
    user_id = redis.get(USER_AUTH_CODE_TEMPLATE % code)

    if not user_id:
        raise AuthorizationCodeInvalid("Invalid authentication code")

    with create_session() as session:
        try:
            user = UserRepo(session).get_by_id(user_id=int(user_id)).get()
        except NoContextError:
            raise UserNotFound(f"User with id {user_id} not found")

    return user


def identify_user_by_refresh_token(token: str) -> User:
    auth_settings: AuthSettings = settings.auth

    try:
        token_payload = jwt.decode(
            token, auth_settings.public_key, algorithms=auth_settings.algorithm
        )
    except PyJWTError:
        raise InvalidTokenException("Invalid token")

    public_id = token_payload.get("public_id", "")

    if not public_id:
        raise InvalidTokenException("Invalid token data")

    with create_session() as session:
        try:
            user = (
                UserRepo(session).get_by_public_id(public_id=public_id).get()
            )
        except NoContextError:
            raise UserNotFound(f"User with public_id {public_id} not found")

    return user
