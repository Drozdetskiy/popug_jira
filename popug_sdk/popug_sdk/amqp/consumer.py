import logging
from functools import partial
from typing import Any

import pika
from pika import spec
from pika.channel import Channel

from popug_sdk.amqp.utils import get_connection_params
from popug_sdk.conf import settings
from popug_sdk.conf.amqp import AMQPSettings

logger = logging.getLogger(settings.project)


class BaseConsumer:
    TIMEOUT = 5

    def __init__(self, config: AMQPSettings):
        self._config = config

        self._connection: pika.SelectConnection | None = None
        self._channel: Channel | None = None
        self._closing: bool = False
        self._consumer_tag: str | None = None

    def _connect(self) -> pika.SelectConnection:
        parameters = get_connection_params(self._config)

        logger.info(
            f"Connecting to host={parameters.host} port={parameters.port} "
            f"virtual_host={parameters.virtual_host}>"
        )
        return pika.SelectConnection(parameters, self._on_connection_open)

    def _on_connection_open(self, connection: pika.SelectConnection) -> None:
        logger.info("Connection opened")

        connection.add_on_close_callback(self._on_connection_closed)
        connection.channel(on_open_callback=self._on_channel_open)

    def _on_connection_closed(
        self, connection: pika.SelectConnection, reason: Exception
    ) -> None:
        if self._closing:
            self._connection.ioloop.stop()  # type: ignore
        else:
            logger.warning(
                f"Connection closed, "
                f"reopen in {self.TIMEOUT} seconds: {reason}"
            )

            connection.add_timeout(self.TIMEOUT, self._reconnect)

    def _reconnect(self) -> None:
        if self._connection:
            self._connection.ioloop.stop()

        if not self._closing:
            self._connection = self._connect()
            self._connection.ioloop.start()

    def _on_channel_open(self, channel: Channel) -> None:
        logger.info("Channel opened")
        self._channel = channel
        self._channel.add_on_close_callback(self._on_channel_close_ok)

        self._setup_exchange(self._channel)

    def _on_channel_close_ok(self, channel: Channel, _: Any) -> None:
        channel.connection.close()

    def _setup_exchange(self, channel: Channel) -> None:
        exchange_name = self._config.exchange.name
        logger.info(f"Declaring exchange {exchange_name}")

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=self._config.exchange.type.value,
            callback=partial(self._setup_queue, channel),
            durable=self._config.exchange.durable,
        )

    def _setup_queue(self, channel: Channel, _: Any) -> None:
        queue_name = self._config.queue.name
        logger.info("Declaring queue %s", queue_name)

        channel.queue_declare(
            queue=queue_name,
            callback=partial(self._on_queue_declareok, channel),
        )

    def _on_queue_declareok(self, channel: Channel, _: Any) -> None:
        for routing_key in self._config.routing_keys:
            logger.info(
                f"Binding {self._config.exchange.name} to "
                f"{self._config.queue.name} with {routing_key}",
            )
            channel.queue_bind(
                queue=self._config.queue.name,
                exchange=self._config.exchange.name,
                routing_key=routing_key,
                callback=partial(self._start_consuming, channel),
            )

    def _start_consuming(self, channel: Channel, _: Any) -> None:
        logger.info("Issuing consumer related RPC commands")
        channel.add_on_cancel_callback(channel.close)
        self._consumer_tag = channel.basic_consume(
            queue=self._config.queue.name,
            on_message_callback=self.on_message,
        )

    def on_message(
        self,
        channel: Channel,
        basic_deliver: spec.Basic.Deliver,
        properties: spec.BasicProperties,
        body: bytes,
    ) -> None:
        logger.debug(
            f"Received message # {basic_deliver.delivery_tag} "
            f"from {properties.app_id}: {body!r}"
        )
        self.process_message(basic_deliver, properties, body)
        channel.basic_ack(basic_deliver.delivery_tag)

    def process_message(
        self,
        basic_deliver: spec.Basic.Deliver,
        properties: spec.BasicProperties,
        body: bytes,
    ) -> None:
        pass

    def run(self) -> None:
        self._connection = self._connect()
        self._connection.ioloop.start()

    def stop(self) -> None:
        logger.info("Stopping")
        self._closing = True

        if self._channel:
            self._channel.basic_cancel(
                consumer_tag=self._consumer_tag,
                callback=lambda _: self._channel.close,
            )
        self._connection.ioloop.start()  # type: ignore
        logger.info("Stopped")
