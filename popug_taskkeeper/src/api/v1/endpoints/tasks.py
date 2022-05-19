from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Security,
)
from schemas.task import (
    NewTaskSchema,
    ReshuffledIdsSchema,
    TaskSchema,
)
from services.exception import TaskNotFound
from services.tasks import (
    add_task as add_task_service,
    complete_task as complete_task_service,
    count_tasks as count_tasks_service,
    get_task as get_task_service,
    get_tasks as get_tasks_service,
    reshuffle as reshuffle_service,
)
from starlette import status

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
    response_model=get_list_response_schema(TaskSchema),
    dependencies=[
        Security(
            check_permissions,
            scopes=["CAN_READ_SELF_TASKS", "CAN_READ_ALL_TASKS"],
        ),
    ],
)
def get_tasks(
    pagination: PagePagination = Depends(PagePagination),
    assignee_id: int | None = Query(None),
) -> dict[str, Any]:
    tasks = get_tasks_service(
        assignee_id=assignee_id,
        limit=pagination.limit,
        offset=pagination.offset,
    )
    count = count_tasks_service(assignee_id=assignee_id)

    return get_response_data(tasks, meta=pagination.get_params(count))


@router.get(
    "/{task_id}",
    response_model=get_response_schema(TaskSchema),
    dependencies=[
        Security(
            check_permissions,
            scopes=["CAN_READ_SELF_TASKS", "CAN_READ_ALL_TASKS"],
        ),
    ],
)
def get_task(task_id: int) -> dict[str, Any]:
    try:
        task = get_task_service(task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return get_response_data(task)


@router.post(
    "/",
    response_model=get_response_schema(TaskSchema, suffix="Details"),
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Security(check_permissions, scopes=["CAN_ASSIGN_NEW_TASKS"]),
    ],
)
def add_task(data: NewTaskSchema) -> dict[str, Any]:
    return get_response_data(add_task_service(data))


# TODO: move logic to patch method when update will be implemented
@router.post(
    "/{task_id}/complete",
    response_model=get_response_schema(TaskSchema, suffix="Completed"),
    status_code=status.HTTP_200_OK,
    dependencies=[
        Security(check_permissions, scopes=["CAN_UPDATE_SELF_TASK"]),
    ],
)
def complete_task(task_id: int) -> dict[str, Any]:
    try:
        task = complete_task_service(task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return get_response_data(task)


# TODO: Make call async with 202 status code
@router.post(
    "/reshuffle",
    status_code=status.HTTP_200_OK,
    response_model=get_response_schema(ReshuffledIdsSchema),
    dependencies=[
        Security(check_permissions, scopes=["CAN_ASSIGN_NEW_TASKS"]),
    ],
)
def reshuffle() -> dict[str, Any]:
    reshuffled_ids = reshuffle_service()
    return get_response_data({"ids": reshuffled_ids})
