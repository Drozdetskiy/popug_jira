from dataclasses import (
    asdict,
    dataclass,
    field,
)
from datetime import (
    datetime,
    timedelta,
)

import jwt
from constants import UserRoles
from utils import (
    dict_factory,
    get_scopes,
)

from popug_sdk.conf import settings


@dataclass
class TokenData:
    pid: str
    username: str
    email: str
    role: UserRoles
    scopes: list[str] = field(init=False)

    def __post_init__(self) -> None:
        self.scopes = get_scopes(self.role)

    def generate_token(self, expires_delta: int) -> str:
        encode_data = asdict(self, dict_factory=dict_factory)
        encode_data["exp"] = datetime.utcnow() + timedelta(expires_delta)

        token: str = jwt.encode(  # type: ignore
            encode_data,
            settings.security.secret_key,
            algorithm=settings.security.algorithm,
        )

        return token
