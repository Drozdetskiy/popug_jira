from popug_sdk.conf.global_settings import (
    Settings as BaseSettings,
    DatabaseSettings,
)


PROGECT_NAME = "{{cookiecutter.project_name}}"


class Settings(BaseSettings):
    project: str = PROGECT_NAME
    use_https = False
    database: DatabaseSettings = DatabaseSettings(
        database_name=f"{PROGECT_NAME}_db"
    )
