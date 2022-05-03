from pydantic import Field

from popug_sdk.conf.amqp import (
    AMQPConfigSettings as BaseAMQPConfigSettings,
    AMQPSettings as BaseAMQPSettings,
    ExchangeSettings,
    QueueSettings,
)
from popug_sdk.conf.db import DatabaseSettings as BaseDatabaseSettings
from popug_sdk.conf.global_settings import Settings as BaseSettings

PROGECT_NAME = "popug_taskkeeper"


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


class TaskBCAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="tasks_bc")
    )


class TaskDSAMQPSettings(BaseAMQPSettings):
    exchange: ExchangeSettings = Field(
        default_factory=lambda: ExchangeSettings(name="tasks_ds")
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


class UserEventsProducerSettings(BaseSettings):
    sleep_time: int = 5


class WorkersSettings(BaseSettings):
    task_events_bc_producer_worker: UserEventsProducerSettings = Field(
        default_factory=UserEventsProducerSettings
    )
    task_events_ds_producer_worker: UserEventsProducerSettings = Field(
        default_factory=UserEventsProducerSettings
    )


class Settings(BaseSettings):
    project: str = PROGECT_NAME
    use_https = False
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    amqp: AMQPConfigSettings = Field(default_factory=AMQPConfigSettings)
    workers: WorkersSettings = Field(default_factory=WorkersSettings)

    class Config(BaseSettings.Config):
        env_prefix = f"{PROGECT_NAME.upper()}_"
