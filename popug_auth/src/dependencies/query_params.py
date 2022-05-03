from fastapi import (
    HTTPException,
    Query,
)
from starlette import status

from popug_sdk.conf import settings


def get_redirect_uri(redirect_uri: str = Query(...)) -> str:
    if redirect_uri not in settings.redirect_uris:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid back url",
        )

    return redirect_uri
