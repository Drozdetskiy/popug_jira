from pydantic import Field

from popug_sdk.conf.amqp import (
    AMQPConfigSettings as BaseAMQPConfigSettings,
    AMQPSettings as BaseAMQPSettings,
    ExchangeSettings,
    QueueSettings,
)
from popug_sdk.conf.db import DatabaseSettings as BaseDatabaseSettings
from popug_sdk.conf.global_settings import Settings as BaseSettings
from popug_sdk.conf.redis import (
    RedisConfigSettings as BaseRedisConfigSettings,
    RedisSettings as BaseRedisSettings,
)

PROGECT_NAME = "popug_accounting"


class DatabaseSettings(BaseDatabaseSettings):
    database_name = f"{PROGECT_NAME}_db"


class UserBCAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="users_bc")
    )
    queue: QueueSettings = Field(
        default_factory=lambda: QueueSettings(
            name=f"{PROGECT_NAME.lower()}.users_bc.all"
        )
    )


class UserDSAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="users_ds")
    )
    queue: QueueSettings = Field(
        default_factory=lambda: QueueSettings(
            name=f"{PROGECT_NAME.lower()}.users_ds.all"
        )
    )


class TaskBCAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="tasks_bc")
    )
    queue: QueueSettings = Field(
        default_factory=lambda: QueueSettings(
            name=f"{PROGECT_NAME.lower()}.tasks_bc.all"
        )
    )


class TaskDSAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="tasks_ds")
    )
    queue: QueueSettings = Field(
        default_factory=lambda: QueueSettings(
            name=f"{PROGECT_NAME.lower()}.tasks_ds.all"
        )
    )


class TaskCostBCAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="taskcosts_bc")
    )


class TransactionBCAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="transactions_bc")
    )


class BillingCycleBCAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="billingcycles_bc")
    )


class AMQPConfigSettings(BaseAMQPConfigSettings):
    users_bc_amqp: UserBCAMQPSettings = Field(
        default_factory=UserBCAMQPSettings
    )
    users_ds_amqp: UserDSAMQPSettings = Field(
        default_factory=UserDSAMQPSettings
    )
    tasks_bc_amqp: TaskBCAMQPSettings = Field(
        default_factory=TaskBCAMQPSettings
    )
    tasks_ds_amqp: TaskDSAMQPSettings = Field(
        default_factory=TaskDSAMQPSettings
    )
    taskcosts_bc_amqp: TaskCostBCAMQPSettings = Field(
        default_factory=TaskCostBCAMQPSettings
    )
    transactions_bc_amqp: TransactionBCAMQPSettings = Field(
        default_factory=TransactionBCAMQPSettings
    )
    billing_cycles_bc_amqp: BillingCycleBCAMQPSettings = Field(
        default_factory=BillingCycleBCAMQPSettings
    )


class CeleryBrokerRedisSettings(BaseRedisSettings):
    db: int = 1


class CeleryResultRedisSettings(BaseRedisSettings):
    db: int = 2


class RedisConfigSettings(BaseRedisConfigSettings):
    celery_broker: CeleryBrokerRedisSettings = Field(
        default_factory=CeleryBrokerRedisSettings
    )
    celery_result: CeleryResultRedisSettings = Field(
        default_factory=CeleryResultRedisSettings
    )


class Settings(BaseSettings):
    project: str = PROGECT_NAME
    use_https = False
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    amqp: AMQPConfigSettings = Field(default_factory=AMQPConfigSettings)
    redis: RedisConfigSettings = Field(default_factory=RedisConfigSettings)

    class Config(BaseSettings.Config):
        env_prefix = f"{PROGECT_NAME.upper()}_"
