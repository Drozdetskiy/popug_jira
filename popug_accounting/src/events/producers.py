from constants import ProducerTypes

from popug_sdk.amqp.producer import BaseProducer
from popug_sdk.conf.amqp import AMQPSettings


class EventsProducer(BaseProducer):
    def open_connection(self) -> None:
        self._open_connection()


_producers: dict[ProducerTypes, EventsProducer] = {}


def init_producer(producer_type: ProducerTypes, config: AMQPSettings) -> None:
    producer = EventsProducer(config, init_exchange=True)
    global _producers
    _producers[producer_type] = producer


def get_producer(producer_type: ProducerTypes) -> EventsProducer:
    producer = _producers.get(producer_type)

    if not producer:
        raise ValueError(f"Producer {producer_type} not found")

    return producer
