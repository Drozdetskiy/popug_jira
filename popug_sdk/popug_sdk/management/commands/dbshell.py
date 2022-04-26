import os
import subprocess

from popug_sdk.conf import settings


def dbshell() -> None:
    os.environ["PGPASSWORD"] = settings.database.password
    subprocess.call(
        [
            "psql",
            "-h",
            settings.database.host,
            "-p",
            str(settings.database.port),
            "-U",
            settings.database.user,
            "-d",
            settings.database.database_name,
        ]
    )
