import os
import pkgutil
from importlib import import_module

import typer

from popug_sdk.conf import settings

init_commands = typer.Typer()


def find_commands(management_dir):
    command_dir = os.path.join(management_dir, "commands")
    return [
        name
        for _, name, is_pkg in pkgutil.iter_modules([command_dir])
        if not is_pkg and not name.startswith("_")
    ]


def get_commands():
    commands = {name: "popug_sdk" for name in find_commands(__path__[0])}
    for config_path in settings.commands_roots:
        path = os.path.join(config_path, "management")
        commands.update({
            name: config_path
            for name in find_commands(path)}
        )
    return commands


for command_name, base_path in get_commands().items():
    module = import_module(f"{base_path}.management.commands.{command_name}")
    command_function = getattr(module, command_name)
    help_text = command_function.__doc__
    init_commands.command(help=help_text)(command_function)
