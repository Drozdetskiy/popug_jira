from __future__ import annotations

import importlib
import os
from functools import lru_cache
from typing import (
    TYPE_CHECKING,
    Type,
)

__all__ = ("settings",)

if TYPE_CHECKING:
    from popug_sdk.conf.global_settings import Settings as BaseSettings


class Settings:
    ENVIRONMENT_VARIABLE = "SETTINGS_MODULE"

    @classmethod
    @lru_cache
    def load(cls) -> BaseSettings:
        settings_module = os.environ.get(
            cls.ENVIRONMENT_VARIABLE, "popug_sdk.conf.global_settings"
        )
        module = importlib.import_module(settings_module)
        settings_class: Type[BaseSettings] = getattr(module, "Settings")
        _settings = settings_class()
        _settings.set_up_logging()

        return _settings


settings = Settings.load()
