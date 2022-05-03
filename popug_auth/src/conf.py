from pydantic import (
    BaseModel,
    Field,
    validator,
)

from popug_sdk.conf.amqp import (
    AMQPConfigSettings as BaseAMQPConfigSettings,
    AMQPSettings as BaseAMQPSettings,
    ExchangeSettings,
)
from popug_sdk.conf.db import DatabaseSettings as BaseDatabaseSettings
from popug_sdk.conf.global_settings import Settings as BaseSettings

PROGECT_NAME = "popug_auth"


class DatabaseSettings(BaseDatabaseSettings):
    database_name = f"{PROGECT_NAME}_db"


class SecuritySettings(BaseModel):
    access_token_expiration: int = 3600  # 1 hour
    refresh_token_expiration: int = 86400  # 1 day
    secret_key: str = "secret_key"
    algorithm: str = "RS256"

    auth_code_expiration: int = 60  # 1 minute

    public_exponent: int = 65537
    key_size: int = 2048

    @validator("secret_key")
    def repair_secret_key(cls, value: str) -> str:
        return value.replace("\\n", "\n")


class UserBCAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="users_bc")
    )


class UserDSAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="users_ds")
    )


class AMQPConfigSettings(BaseAMQPConfigSettings):
    users_bc_amqp: UserBCAMQPSettings = Field(
        default_factory=UserBCAMQPSettings
    )
    users_ds_amqp: UserDSAMQPSettings = Field(
        default_factory=UserDSAMQPSettings
    )


class Settings(BaseSettings):
    project: str = PROGECT_NAME
    use_https = False
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    redis_configs: list[str] = Field(default_factory=lambda: ["default"])
    redirect_uris: list[str] = Field(default_factory=list)
    amqp: AMQPConfigSettings = Field(default_factory=AMQPConfigSettings)

    class Config(BaseSettings.Config):
        env_prefix = f"{PROGECT_NAME.upper()}_"
