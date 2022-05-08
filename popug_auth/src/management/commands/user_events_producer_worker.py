# from events.user.producer import UserEventsProducer

# from popug_sdk.conf import settings
# from popug_sdk.conf.amqp import AMQPConfigSettings
# from popug_sdk.db import create_session


def user_events_producer_worker() -> None:
    pass
    # amqp_config_settings: AMQPConfigSettings = settings.amqp
    # producer = UserEventsProducer(amqp_config_settings.default)

    # while True:
    #     with create_session() as session:
    #         repo = UserEventLogsRepo(session).get_for_sending(producer.send)
    #         messages = prepare_messages(repo.get())
    #         producer.publish(messages, ...)
    #         repo.mark_as_sent().apply()

    # sleep(...)
