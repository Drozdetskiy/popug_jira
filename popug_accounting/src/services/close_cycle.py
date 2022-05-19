from events.billing_cycle.send_event import (
    send_billing_cycle_closed_event,
    send_billing_cycle_started_event,
)
from repos.billing_cycle import BillingCycleRepo

from popug_sdk.db import create_session


def close_cycle() -> None:
    with create_session() as session:
        closed_cycle = (
            BillingCycleRepo(session).get_last(lock=True).close().get()
        )
        cycle = BillingCycleRepo(session).create_active().apply()

    send_billing_cycle_closed_event(closed_cycle)
    send_billing_cycle_started_event(cycle)
