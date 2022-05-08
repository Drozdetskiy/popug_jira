from conf import SecuritySettings
from pydantic import BaseModel
from schemas.user import UserInfoSchema

from popug_sdk.conf import settings

security_settings: SecuritySettings = settings.security


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    scopes: list[str]
    info: UserInfoSchema
    token_type: str = "bearer"
    expires_in: int = security_settings.access_token_expiration
