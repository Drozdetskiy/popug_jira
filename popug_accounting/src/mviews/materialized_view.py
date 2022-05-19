from typing import (
    Any,
    Iterable,
)

from sqlalchemy import (
    Column,
    MetaData,
    Table,
)
from sqlalchemy.orm import Session
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.sql import Select

from popug_sdk.db import (
    create_session,
    mapper_registry,
)


def create_materialized_view(
    name: str,
    selectable: Select,
    primary_keys: Iterable[Any],
    metadata: MetaData = mapper_registry.metadata,
) -> Table:
    table = Table(name, metadata)

    for c in selectable.c:
        table.append_column(Column(c.name, c.type))

    table.append_constraint(
        PrimaryKeyConstraint(*[c.name for c in primary_keys])
    )

    return table


def refresh_materialized_view(
    name: str, session: Session | None = None
) -> None:
    with create_session(session) as session:
        session.execute(f"REFRESH MATERIALIZED VIEW {name}")  # type: ignore
