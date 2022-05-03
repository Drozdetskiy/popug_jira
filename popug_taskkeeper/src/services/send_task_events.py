from constants import EventTypes
from events.utils import (
    get_routing_key,
    prepare_message,
)
from models import EventLog
from repos.event_logs import TaskEventLogsListRepo

from popug_sdk.amqp.producer import BaseProducer
from popug_sdk.db import create_session


def send_task_events(
    producer: BaseProducer, event_type: EventTypes
) -> list[EventLog]:
    with create_session() as session:
        processed_events = []

        repo = TaskEventLogsListRepo(session)
        repo.get_unprocessed_events(event_type, lock=True, skip_locked=True)

        try:
            for event_log in repo.get():
                message = prepare_message(event_log)
                routing_key = get_routing_key(event_log)
                producer.publish_message(message, routing_key)
                processed_events.append(event_log)
        finally:
            repo(processed_events).mark_as_sent().apply()  # type: ignore

        return processed_events
