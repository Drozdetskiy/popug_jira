from constants import EventTypes

from popug_sdk.amqp.producer import BaseProducer
from popug_sdk.conf import settings
from popug_sdk.conf.amqp import AMQPSettings


class TaskEventsProducer(BaseProducer):
    def open_connection(self) -> None:
        self._open_connection()


_producers: dict[EventTypes, TaskEventsProducer | None] = {
    EventTypes.BUSINESS_CALL: None,
    EventTypes.DATA_STREAMING: None,
}


_config_map: dict[EventTypes, AMQPSettings] = {
    EventTypes.BUSINESS_CALL: settings.amqp.tasks_bc_amqp,
    EventTypes.DATA_STREAMING: settings.amqp.tasks_ds_amqp,
}


def create_producer(event_type: EventTypes) -> TaskEventsProducer:
    config: AMQPSettings = _config_map[event_type]
    producer = TaskEventsProducer(config, init_exchange=True)
    global _producers
    _producers[event_type] = producer

    return producer


def get_producer(event_type: EventTypes) -> TaskEventsProducer:
    producer = _producers[event_type]

    if not producer:
        return create_producer(event_type)

    return producer
