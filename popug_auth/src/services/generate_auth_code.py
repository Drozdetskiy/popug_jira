from typing import TYPE_CHECKING
from uuid import uuid4

from constants import USER_AUTH_CODE_TEMPLATE
from models import User

from popug_sdk.conf import settings

if TYPE_CHECKING:
    from redis import Redis as BaseRedis

    Redis = BaseRedis[str]
else:
    from redis import Redis


# TODO: make auth code generation secure (add proof key for code exchange)
def generate_auth_code(redis: Redis, user: User) -> str:
    auth_code = uuid4().hex
    auth_code_key = USER_AUTH_CODE_TEMPLATE % auth_code
    redis.set(
        auth_code_key, user.id, ex=settings.security.auth_code_expiration
    )

    return auth_code
