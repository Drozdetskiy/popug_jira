from conf import AMQPConfigSettings
from events.user.consumers import UserEventsConsumer
from services.user_events_service import process_user_event_message

from popug_sdk.conf import settings


def user_data_streaming_events_consumer():
    print(settings.amqp.users_ds_amqp)
    # TODO: process events exceptions. MB add deadletter queue
    amqp_config_settings: AMQPConfigSettings = settings.amqp
    consumer = UserEventsConsumer(
        amqp_config_settings.users_ds_amqp,
        callback=process_user_event_message,
    )
    consumer.run()
