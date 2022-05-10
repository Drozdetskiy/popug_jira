import os

os.environ.setdefault("SETTINGS_MODULE", "src.conf")  # noqa

from popug_sdk.management import init_commands

if __name__ == "__main__":
    init_commands()
