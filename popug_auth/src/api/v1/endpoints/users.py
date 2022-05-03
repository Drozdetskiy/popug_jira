from typing import Any

from constants import UserRoles
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Security,
)
from schemas.user import (
    UserAddSchema,
    UserInfoSchema,
    UserPublicIDSchema,
    UserUpdateSchema,
)
from services.exceptions import (
    UserAlreadyExists,
    UserNotFound,
)
from services.users import (
    change_user_role as change_user_role_service,
    count_users as count_users_service,
    create_user as create_user_service,
    delete_user as delete_user_service,
    get_user as get_user_service,
    get_users as get_users_service,
)
from starlette import status
from utils import get_scopes

from popug_sdk.auth.dependencies.permissions import check_permissions
from popug_sdk.dependencies.pagination import PagePagination
from popug_sdk.response.response import get_response_data
from popug_sdk.schemas.response_schema import (
    get_list_response_schema,
    get_response_schema,
)

router = APIRouter()


@router.get(
    "/",
    response_model=get_list_response_schema(UserInfoSchema),
    dependencies=[
        Security(check_permissions, scopes=get_scopes(UserRoles.EMPLOYEE))
    ],
)
def get_users(
    pagination: PagePagination = Depends(PagePagination),
) -> dict[str, Any]:
    users = get_users_service(limit=pagination.limit, offset=pagination.offset)
    count = count_users_service()

    return get_response_data(users, meta=pagination.get_params(count))


@router.get(
    "/{user_id}",
    response_model=get_response_schema(UserInfoSchema, suffix="Details"),
    dependencies=[
        Security(check_permissions, scopes=get_scopes(UserRoles.EMPLOYEE))
    ],
)
def get_user(user_id: int) -> dict[str, Any]:
    try:
        user = get_user_service(user_id=user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return get_response_data(user)


@router.post(
    "/",
    response_model=get_response_schema(UserInfoSchema, suffix="Create"),
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Security(check_permissions, scopes=get_scopes(UserRoles.ADMIN))
    ],
)
def create_user(data: UserAddSchema) -> dict[str, Any]:
    try:
        user = create_user_service(data)
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    return get_response_data(user)


# TODO: implement patch not only for role
@router.patch(
    "/{user_id}",
    response_model=get_response_schema(UserInfoSchema, suffix="Patch"),
    dependencies=[
        Security(check_permissions, scopes=get_scopes(UserRoles.ADMIN))
    ],
)
def update_user(
    user_id: int,
    data: UserUpdateSchema,
) -> dict[str, Any]:
    try:
        user = change_user_role_service(user_id=user_id, role=data.role)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return get_response_data(user)


@router.delete(
    "/{user_id}",
    response_model=get_response_schema(UserPublicIDSchema, suffix="Delete"),
    dependencies=[
        Security(check_permissions, scopes=get_scopes(UserRoles.ADMIN))
    ],
)
def delete_user(user_id: int) -> dict[str, Any]:
    try:
        user = delete_user_service(user_id=user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return get_response_data(user)
