from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Security,
)
from schemas.user import UserInfoSchema
from services.exception import UserNotFound
from services.users import get_user_by_public_id
from starlette import status

from popug_sdk.auth.dependencies.permissions import check_permissions
from popug_sdk.auth.dependencies.token import get_token_data
from popug_sdk.response.response import get_response_data
from popug_sdk.schemas.response_schema import get_response_schema

router = APIRouter()


@router.get(
    "/me",
    response_model=get_response_schema(UserInfoSchema),
    dependencies=[
        Security(
            check_permissions,
            scopes=["CAN_READ_USERS"],
        ),
    ],
)
def get_me(
    token_data: dict[str, Any] = Depends(get_token_data),
) -> dict[str, Any]:
    public_id = token_data.get("public_id")
    if not public_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No public_id in token data",
        )

    try:
        user = get_user_by_public_id(public_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return get_response_data(user)
