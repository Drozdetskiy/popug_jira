from pydantic import BaseModel

from popug_sdk.conf.constants import (
    LOCALHOST,
    PortType,
)


class RedisSettings(BaseModel):
    host: str = LOCALHOST
    port: PortType = 6379
    db: int = 0
