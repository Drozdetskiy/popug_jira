from pydantic import BaseModel

from popug_sdk.conf.constants import (
    BASE_NAME,
    LOCALHOST,
    PortType,
)


class DatabaseSettings(BaseModel):
    enabled: bool = False
    host: str = LOCALHOST
    port: PortType = 5432
    user: str = "postgres"
    password: str = "postgres"
    database_name: str = f"{BASE_NAME}_db"
