import typer
from alembic.command import (
    downgrade,
    upgrade,
)
from alembic.config import Config

from popug_sdk.conf import settings


def migrate(
    revision: str = typer.Option("head"), down: bool = typer.Option(False)
) -> None:
    alembic_config = Config(settings.alembic.config)
    method = downgrade if down else upgrade
    method(alembic_config, revision)
