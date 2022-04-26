import os
import pkgutil
from importlib import import_module
from typing import (
    Callable,
    NoReturn,
)

import typer

from popug_sdk.conf import settings

init_commands = typer.Typer()


def find_commands(management_dir: str) -> list[str]:
    command_dir = os.path.join(management_dir, "commands")
    return [
        name
        for _, name, is_pkg in pkgutil.iter_modules([command_dir])
        if not is_pkg and not name.startswith("_")
    ]


def get_commands() -> dict[str, str]:
    commands = {name: "popug_sdk" for name in find_commands(__path__[0])}
    for config_path in settings.commands_roots:
        path = os.path.join(config_path, "management")
        commands.update({name: config_path for name in find_commands(path)})

    return commands


def get_command_fail(exc: Exception, name: str) -> Callable[[], NoReturn]:
    def _command_fail() -> NoReturn:
        """Failed to load command"""
        raise exc

    _command_fail.__name__ = name

    return _command_fail


for command_name, base_path in get_commands().items():
    try:
        module = import_module(
            f"{base_path}.management.commands.{command_name}"
        )
    except ModuleNotFoundError as exc:
        command_function = get_command_fail(exc, command_name)
    else:
        command_function = getattr(module, command_name)

    help_text = command_function.__doc__
    init_commands.command(help=help_text)(command_function)
