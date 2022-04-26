from os import listdir
from os.path import (
    isfile,
    join,
)

import typer
from alembic.command import revision
from alembic.config import Config

from popug_sdk.conf import settings


def _get_revision_id(directory: str) -> str:
    versions_dir = join(directory, "versions")
    max_revision = 0
    for file in listdir(versions_dir):
        if isfile(join(versions_dir, file)):
            file_revision, *_ = file.split("_", 1)
            if file_revision.isdigit() and int(file_revision) > max_revision:
                max_revision = int(file_revision)
    return str(max_revision).rjust(4, "0")


def _get_next_revision_id(directory: str) -> str:
    revision_id = _get_revision_id(directory)
    return str(int(revision_id) + 1).rjust(4, "0")


def makemigrations(message: str = typer.Option("auto")) -> None:
    revision(
        Config(settings.alembic.config),
        message=message,
        autogenerate=True,
        rev_id=_get_next_revision_id(settings.alembic.directory),
    )
