from mviews import Balance
from repos.balance import BalanceListRepo

from popug_sdk.db import create_session


def get_balances(
    billing_cycle_id: int, user_id: int, limit: int, offset: int
) -> list[Balance]:
    with create_session() as session:
        return (
            BalanceListRepo(session)
            .get_list(
                billing_cycle_id=billing_cycle_id,
                user_id=user_id,
                limit=limit,
                offset=offset,
            )
            .get()
        )


def count_balances(billing_cycle_id: int, user_id: int) -> int:
    with create_session() as session:
        return BalanceListRepo(session).count_all(
            billing_cycle_id=billing_cycle_id,
            user_id=user_id,
        )
