from pydantic import (
    BaseModel,
    Field,
)

from popug_sdk.conf.constants import (
    LOCALHOST,
    PortType,
)


class RedisSettings(BaseModel):
    host: str = LOCALHOST
    port: PortType = 6379
    db: int = 0


class RedisConfigSettings(BaseModel):
    default: RedisSettings = Field(default_factory=RedisSettings)
