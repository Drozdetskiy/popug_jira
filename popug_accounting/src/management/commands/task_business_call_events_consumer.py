from conf import AMQPConfigSettings
from constants import ProducerTypes
from events.consumers import EventsConsumer
from events.producers import init_producer
from services.task_events_services import process_task_event_message

from popug_sdk.conf import settings


def task_business_call_events_consumer() -> None:
    # TODO: process events exceptions. MB add deadletter queue
    amqp_config: AMQPConfigSettings = settings.amqp
    init_producer(ProducerTypes.TASKCOSTS_BC, amqp_config.taskcosts_bc_amqp)
    init_producer(
        ProducerTypes.TRANSACTIONS_BC, amqp_config.transactions_bc_amqp
    )
    amqp_config_settings: AMQPConfigSettings = settings.amqp
    consumer = EventsConsumer(
        amqp_config_settings.tasks_bc_amqp, callback=process_task_event_message
    )
    consumer.run()
