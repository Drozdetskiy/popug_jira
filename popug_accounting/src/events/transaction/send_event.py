from datetime import datetime

from constants import ProducerTypes
from dto.transaction import TransactionDTO
from events.producers import get_producer
from events.utils import get_routing_key

from popug_schema_registry.models.v1.transaction_added_event_schema import (
    TransactionAddedEventSchema,
)


def send_transaction_added_event(transaction_dto: TransactionDTO) -> None:
    producer = get_producer(ProducerTypes.TRANSACTIONS_BC)
    event = TransactionAddedEventSchema(
        data={
            "public_id": transaction_dto.public_id,
            "task_public_id": transaction_dto.task
            and transaction_dto.task.public_id,
            "user_public_id": transaction_dto.user.public_id,
            "debit": transaction_dto.debit,
            "credit": transaction_dto.credit,
            "type": transaction_dto.type,
        },
        produced_at=datetime.utcnow(),
    )
    producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),
    )
