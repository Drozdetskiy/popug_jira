import logging
from typing import (
    Any,
    Callable,
)

from popug_sdk.amqp.consumer import BaseConsumer
from popug_sdk.conf import settings
from popug_sdk.conf.amqp import AMQPSettings

logger = logging.getLogger(settings.project)


class EventsConsumer(BaseConsumer):
    def __init__(
        self, config: AMQPSettings, callback: Callable[[Any], Any]
    ) -> None:
        self._config = config
        self._callback = callback
        super().__init__(config)

    def process_message(self, _: Any, __: Any, body: bytes) -> None:
        try:
            self._callback(body)
        except Exception as exc:
            logger.error(f"Error during processing: {exc}")
            raise
