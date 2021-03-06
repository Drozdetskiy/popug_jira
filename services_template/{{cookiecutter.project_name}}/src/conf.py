from popug_sdk.conf.global_settings import Settings as BaseSettings

PROGECT_NAME = "{{cookiecutter.project_name}}"


class Settings(BaseSettings):
    project: str = PROGECT_NAME
    use_https = False

    class Config(BaseSettings.Config):
        env_prefix = f"{PROGECT_NAME.upper()}_"
