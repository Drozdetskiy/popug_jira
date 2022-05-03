from typing import (
    TYPE_CHECKING,
    Any,
)

from dependencies.query_params import get_redirect_uri
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from schemas.token import TokenResponseSchema
from services.exceptions import (
    AuthorizationCodeInvalid,
    InvalidTokenException,
    UserNotFound,
)
from services.generate_auth_code import generate_auth_code
from services.identify_user import (
    identify_user_by_auth_code,
    identify_user_by_beak_shape,
    identify_user_by_refresh_token,
)
from services.issue_token_pair import issue_token_pair
from starlette import status
from starlette.responses import RedirectResponse
from utils import get_scopes

from popug_sdk.dependencies.redis import get_redis

if TYPE_CHECKING:
    from redis import Redis as BaseRedis

    Redis = BaseRedis[str]
else:
    from redis import Redis

router = APIRouter()


@router.get("/authorize")
def authorize(
    beak_shape: str,
    response_type: str,
    redirect_uri: str = Depends(get_redirect_uri),
    redis: Redis = Depends(get_redis()),
) -> RedirectResponse:
    if response_type != "code":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid response type",
        )

    try:
        user = identify_user_by_beak_shape(beak_shape)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    auth_code = generate_auth_code(redis, user)

    return RedirectResponse(url=f"{redirect_uri}?code={auth_code}")


@router.post(
    "/token",
    response_model=TokenResponseSchema,
)
def token(
    grant_type: str = Query(...),
    _: str = Query("", alias="client_id"),
    __: str = Query("", alias="client_secret"),
    code: str = Query(None),
    refresh_token: str = Query(None),
    redis: Redis = Depends(get_redis()),
) -> dict[str, Any]:
    if grant_type == "authorization_code":
        if code is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing authorization code",
            )

        try:
            user = identify_user_by_auth_code(redis, code)
        except (AuthorizationCodeInvalid, UserNotFound):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif grant_type == "refresh_token":
        if refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing refresh token",
            )

        try:
            user = identify_user_by_refresh_token(refresh_token)
        except (UserNotFound, InvalidTokenException):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid grant type",
        )

    token_pair = issue_token_pair(user)

    return {
        "access_token": token_pair.access_token,
        "refresh_token": token_pair.refresh_token,
        "scopes": get_scopes(user.role),
        "info": {
            "pid": user.pid,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        },
    }
