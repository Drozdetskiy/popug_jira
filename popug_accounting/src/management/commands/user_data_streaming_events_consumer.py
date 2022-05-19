from conf import AMQPConfigSettings
from events.consumers import EventsConsumer
from services.user_events_service import process_user_event_message

from popug_sdk.conf import settings


def user_data_streaming_events_consumer() -> None:
    # TODO: process events exceptions. MB add deadletter queue
    amqp_config_settings: AMQPConfigSettings = settings.amqp
    consumer = EventsConsumer(
        amqp_config_settings.users_ds_amqp, callback=process_user_event_message
    )
    consumer.run()
