import logging.config
from typing import Any

from pydantic import (
    BaseModel,
    BaseSettings,
    Field,
)

__all__ = ("Settings",)

from popug_sdk.conf.amqp import AMQPSettings
from popug_sdk.conf.constants import (
    BASE_NAME,
    LOCALHOST,
    LOG_LEVEL,
    PortType,
)
from popug_sdk.conf.db import DatabaseSettings
from popug_sdk.conf.redis import RedisSettings


class AppSettings(BaseModel):
    debug: bool = False
    instance: str = "src.main:app"
    app_schema: str = "http"
    app_host: str = LOCALHOST
    app_port: PortType = "8080"


class AlembicSettings(BaseModel):
    config: str = "src/alembic/alembic.ini"
    directory: str = "src/alembic"


class Settings(BaseSettings):
    project: str = BASE_NAME
    version: str = "0.0.1"
    debug: bool = False
    use_https: bool = True
    log_level: str = LOG_LEVEL
    tag_groups: list[dict[str, Any]] = Field(default_factory=list)
    commands_roots: list[str] = Field(default_factory=lambda: ["src"])

    app: AppSettings = Field(default_factory=AppSettings)
    alembic: AlembicSettings = Field(default_factory=AlembicSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    amqp: dict[str, AMQPSettings] = Field(default_factory=dict)
    redis: dict[str, RedisSettings] = Field(default_factory=dict)

    @property
    def database_dsn(self) -> str:
        database_dsn_template = (
            "postgresql://"
            "{database_user}:{database_password}@"
            "{database_host}:{database_port}/"
            "{database_name}"
        )

        return database_dsn_template.format(
            database_user=self.database.user,
            database_password=self.database.password,
            database_host=self.database.host,
            database_port=self.database.port,
            database_name=self.database.database_name,
        )

    @property
    def logging(self) -> dict[str, Any]:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "consoleFormatter": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "[%(process)d] [%(asctime)s] [%(levelname)s] %(name)s -> %(message)s",  # noqa
                },
                "access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": "[%(asctime)s] [%(levelname)s] %(name)s -> '%(request_line)s' %(status_code)s",  # noqa
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "consoleFormatter",
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                self.project: {
                    "handlers": ["console"],
                    "level": self.log_level,
                },
                "uvicorn.error": {"level": "INFO"},
                "uvicorn": {
                    "handlers": ["access"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }

    class Config:
        env_prefix = f"{BASE_NAME.upper()}_"
        env_file = ".env"
        env_nested_delimiter = "__"

    def set_up_logging(self) -> None:
        logging.config.dictConfig(self.logging)
