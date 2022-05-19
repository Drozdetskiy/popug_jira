from repos.billing_cycle import BillingCycleRepo

from popug_sdk.db import create_session


def generate_test_data() -> None:
    with create_session() as session:
        repo = BillingCycleRepo(session)
        cycle = repo.get_last().context()

        if not cycle:
            repo.create_active().apply()
