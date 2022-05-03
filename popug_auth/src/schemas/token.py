from conf import SecuritySettings
from constants import UserRoles
from pydantic import BaseModel

from popug_sdk.conf import settings

security_settings: SecuritySettings = settings.security


class UserInfo(BaseModel):
    pid: str
    username: str
    email: str
    role: UserRoles


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    scopes: list[str]
    info: UserInfo
    token_type: str = "bearer"
    expires_in: int = security_settings.access_token_expiration
