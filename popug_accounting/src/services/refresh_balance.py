from mviews import Balance
from mviews.materialized_view import refresh_materialized_view

from popug_sdk.db import create_session


def refresh_balance() -> None:
    with create_session() as session:
        refresh_materialized_view(Balance.__table__.name, session)
