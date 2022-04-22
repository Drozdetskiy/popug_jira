import subprocess

import typer


def test(directory: str = typer.Option("")):
    exit(subprocess.call([
        "python",
        "-m",
        "pytest",
        directory,
        "-s",
    ]))
