from collections import namedtuple

from conf import SecuritySettings
from models import User
from repos.user_refresh_token import UserRefreshTokenRepo
from token_data import TokenData

from popug_sdk.conf import settings
from popug_sdk.db import create_session

TokenPair = namedtuple("TokenPair", ["access_token", "refresh_token"])


def issue_token_pair(user: User) -> TokenPair:
    security_settings: SecuritySettings = settings.security
    token_data = TokenData(
        public_id=user.public_id,
        username=user.username,
        email=user.email,
        role=user.role,
    )
    access_token = token_data.generate_token(
        security_settings.access_token_expiration
    )
    refresh_token = token_data.generate_token(
        security_settings.refresh_token_expiration
    )

    with create_session() as session:
        UserRefreshTokenRepo(session).upsert_refresh_token(
            user.id, refresh_token
        ).apply()

    return TokenPair(access_token, refresh_token)
