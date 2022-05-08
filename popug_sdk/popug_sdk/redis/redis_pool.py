from typing import Iterable

from redis import ConnectionPool

from popug_sdk.conf.redis import (
    RedisConfigSettings,
    RedisSettings,
)

_redis_pools: dict[str, ConnectionPool] = {}


def init_redis_pool(
    config_names: list[str], config: RedisConfigSettings
) -> None:
    close_redis_pool(config_names)
    _redis_pools.clear()

    for config_name in config_names:
        redis_pool_config: RedisSettings = getattr(config, config_name)
        _redis_pools[config_name] = ConnectionPool(
            host=redis_pool_config.host,
            port=redis_pool_config.port,
            db=redis_pool_config.db,
        )


def close_redis_pool(config_names: Iterable[str]) -> None:
    for config_name in config_names:
        pool = _redis_pools.get(config_name)
        if pool:
            pool.disconnect()


def get_redis_pool(config_name: str = "default") -> ConnectionPool:
    if not _redis_pools:
        raise Exception("Call create_redis_pool() first")

    return _redis_pools[config_name]
