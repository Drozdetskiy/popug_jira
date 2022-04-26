import subprocess

import typer


def test(directory: str = typer.Option("")) -> None:
    exit(
        subprocess.call(
            [
                "python",
                "-m",
                "pytest",
                directory,
                "-s",
            ]
        )
    )
