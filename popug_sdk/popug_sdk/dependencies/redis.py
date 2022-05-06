from typing import Callable

from redis import Redis

from popug_sdk.redis.redis_pool import get_redis_pool


def get_redis(config_name: str = "default") -> Callable[[], Redis]:
    def _get_redis() -> Redis:
        return Redis(connection_pool=get_redis_pool(config_name))

    return _get_redis
