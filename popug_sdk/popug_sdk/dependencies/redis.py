from typing import (
    TYPE_CHECKING,
    Callable,
)

from popug_sdk.redis.redis_pool import get_redis_pool

if TYPE_CHECKING:
    from redis import Redis as BaseRedis

    Redis = BaseRedis[bytes]
else:
    from redis import Redis


def get_redis(config_name: str = "default") -> Callable[[], Redis]:
    def _get_redis() -> Redis:
        return Redis(connection_pool=get_redis_pool(config_name))

    return _get_redis
