from events.billing_cycle.send_event import send_billing_cycle_processed_event
from repos.billing_cycle import BillingCycleRepo
from repos.transaction import TransactionsListRepo

from popug_sdk.db import create_session


def process_cycle() -> None:
    from src.tasks import send_payment

    with create_session() as session:
        repo = BillingCycleRepo(session)
        cycle = repo.get_last_closed(lock=True).context()

        if cycle:
            _user_ids = TransactionsListRepo(session).get_all_users_in_cycle(
                cycle.id
            )
            user_ids = [user_id[0] for user_id in _user_ids]
            for user_id in user_ids:
                send_payment.delay(user_id, cycle.id)

            cycle = repo.process().apply()

    if cycle:
        send_billing_cycle_processed_event(cycle)
