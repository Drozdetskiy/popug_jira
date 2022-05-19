from typing import (
    Any,
    Callable,
)

from popug_sdk.amqp.consumer import BaseConsumer
from popug_sdk.conf.amqp import AMQPSettings


class UserEventsConsumer(BaseConsumer):
    def __init__(
        self, config: AMQPSettings, callback: Callable[[Any], Any]
    ) -> None:
        self._config = config
        self._callback = callback
        super().__init__(config)

    def process_message(self, _: Any, __: Any, body: bytes) -> None:
        self._callback(body)
