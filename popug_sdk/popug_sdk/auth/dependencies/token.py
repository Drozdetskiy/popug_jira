from typing import Any

import jwt
from fastapi import (
    Depends,
    HTTPException,
)
from jwt import PyJWTError
from starlette import status

from popug_sdk.auth.oauth_schema import oauth2_schema
from popug_sdk.conf import settings
from popug_sdk.conf.auth import AuthSettings


def get_token_data(token: str = Depends(oauth2_schema)) -> dict[str, Any]:
    token = token.replace("Bearer ", "")

    auth_settings: AuthSettings = settings.auth

    try:
        token_payload: dict[str, Any] = jwt.decode(
            token, auth_settings.public_key, algorithms=auth_settings.algorithm
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return token_payload
