import typer
from alembic.command import init
from alembic.config import Config

from popug_sdk.conf import settings


def init_alembic(directory: str = typer.Option(None)) -> None:
    directory = directory or settings.alembic.directory
    init(Config(settings.alembic.config), directory)
