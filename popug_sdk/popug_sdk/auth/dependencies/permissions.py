from typing import Any

from fastapi import (
    Depends,
    HTTPException,
)
from fastapi.security import SecurityScopes
from starlette import status

from popug_sdk.auth.dependencies.token import get_token_data


def check_permissions(
    security_scopes: SecurityScopes,
    token_data: dict[str, Any] = Depends(get_token_data),
) -> None:
    token_scopes = token_data.get("scopes", [])

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource",
            )
