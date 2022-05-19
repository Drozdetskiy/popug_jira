from repos.billing_cycle import (
    BillingCycleListRepo,
    BillingCycleRepo,
)
from repos.exceptions import BillingCycleNotFound

from popug_sdk.db import create_session
from popug_sdk.repos.base import NoContextError


def get_billing_cycles(limit: int, offset: int):
    with create_session() as session:
        return BillingCycleListRepo(session).get_list(limit, offset).get()


def count_billing_cycles():
    with create_session() as session:
        return BillingCycleListRepo(session).count_all()


def get_billing_cycle(billing_cycle_id: int):
    with create_session() as session:
        try:
            billing_cycle = (
                BillingCycleRepo(session).get_by_id(billing_cycle_id).get()
            )
        except NoContextError:
            raise BillingCycleNotFound(
                f"Billing cycle {billing_cycle_id} not found"
            )

    return billing_cycle
