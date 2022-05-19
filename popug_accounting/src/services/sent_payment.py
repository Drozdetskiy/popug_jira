from events.transaction.send_event import send_transaction_added_event
from logic import send_email_notification
from repos.billing_cycle import BillingCycleRepo
from repos.transaction import (
    TransactionRepo,
    TransactionsListRepo,
)

from popug_schema_registry.models.v1.transaction_added_event_schema import (
    TransactionTypes,
)
from popug_sdk.db import create_session


def sent_payment(user_id: int, billing_cycle_id: int) -> None:
    with create_session() as session:
        debit, credit = TransactionsListRepo(
            session
        ).get_balance_for_user_by_cycle(user_id, billing_cycle_id)

        payment = credit + debit

        new_billing_cycle = BillingCycleRepo(session).get_last().get()

        if payment <= 0:
            transaction = (
                TransactionRepo(session)
                .add(
                    debit=payment,
                    type=TransactionTypes.PAYMENT,
                    billing_cycle_id=new_billing_cycle.id,
                    user_id=user_id,
                )
                .apply()
            )
            transaction_dto = transaction.to_dto()
        else:
            transaction = (
                TransactionRepo(session)
                .add(
                    credit=payment,
                    type=TransactionTypes.PAYMENT,
                    billing_cycle_id=new_billing_cycle.id,
                    user_id=user_id,
                )
                .apply()
            )
            transaction_dto = transaction.to_dto()
            send_email_notification(transaction_dto)

    send_transaction_added_event(transaction_dto)
