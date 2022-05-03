from dataclasses import asdict

from constants import (
    EventTypes,
    TaskStatus,
)
from dto.task import TaskDTO
from events.task.producers import get_producer
from events.utils import get_routing_key
from models import Task
from pydantic import BaseModel
from repos.task import (
    TaskRepo,
    TasksListRepo,
)
from repos.user import UsersListRepo
from schemas.events import (
    TaskAssignedEventSchema,
    TaskCompletedEventSchema,
    TaskCreatedEventSchema,
)
from services.exception import (
    TaskNotFound,
    WrongTaskStatus,
)
from sqlalchemy.orm import Session

from popug_sdk.db import create_session
from popug_sdk.repos.base import NoContextError


def get_tasks(
    limit: int, offset: int, assignee_id: int | None = None
) -> list[TaskDTO]:
    with create_session() as session:
        tasks = (
            TasksListRepo(session)
            .get_list(limit, offset, assignee_id=assignee_id)
            .get()
        )

        tasks_dto = [task.to_dto() for task in tasks]

    return tasks_dto


def get_task(task_id: int) -> TaskDTO:
    with create_session() as session:
        try:
            task = TaskRepo(session).get_by_id(task_id).get()
        except NoContextError:
            raise TaskNotFound(f"Task {task_id} not found")

        return task.to_dto()


def count_tasks(
    assignee_id: int | None = None, session: Session = None
) -> int:
    with create_session(session) as session:
        return TasksListRepo(session).count_all(assignee_id)


def add_task(data: BaseModel) -> TaskDTO:
    with create_session() as session:
        task_repo = TaskRepo(session).create_task(**data.dict())
        task = task_repo.get()
        task_data = asdict(task)

        old_assignee_public_id = task.assignee and task.assignee.public_id

        user, *_ = UsersListRepo(session).get_random_employees(lock=True).get()
        task = task_repo.assign_to_user(user.id).apply()
        task_dto = task.to_dto()

    event = TaskCreatedEventSchema(data=task_data)
    ds_producer = get_producer(EventTypes.DATA_STREAMING)
    ds_producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),
    )

    bc_producer = get_producer(EventTypes.BUSINESS_CALL)
    event = TaskAssignedEventSchema(
        data={
            "public_id": task.public_id,
            "old_assignee_public_id": old_assignee_public_id,
            "new_assignee_public_id": user.public_id,
        }
    )
    bc_producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),
    )

    return task_dto


def assign_task(task_id: int) -> TaskDTO:
    with create_session() as session:
        task_repo = TaskRepo(session).get_by_id(task_id, lock=True, of=Task)
        try:
            task = task_repo.get()
        except NoContextError:
            raise TaskNotFound(f"Task {task_id} not found")

        if task.status != TaskStatus.OPEN:
            raise WrongTaskStatus(
                f"Task {task_id} has wrong status {task.status}"
            )

        old_assignee_public_id = task.assignee.public_id
        user, *_ = UsersListRepo(session).get_random_employees(lock=True).get()
        task = task_repo.assign_to_user(user.id).apply()

    producer = get_producer(EventTypes.BUSINESS_CALL)
    event = TaskAssignedEventSchema(
        data={
            "public_id": task.public_id,
            "old_assignee_public_id": old_assignee_public_id,
            "new_assignee_public_id": user.public_id,
        }
    )
    producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),
    )

    return task.to_dto()


def reshuffle() -> list[int]:
    with create_session() as session:
        tasks_list = TasksListRepo(session).get_all_opened().get()
        task_ids = [task.id for task in tasks_list]

    # TODO: Move logic to celery
    for task_id in task_ids:
        assign_task(task_id)

    return task_ids


def complete_task(task_id: int) -> TaskDTO:
    with create_session() as session:
        task_repo = TaskRepo(session)

        try:
            task = task_repo.get_by_id(task_id, lock=True, of=Task).get()
        except NoContextError:
            raise TaskNotFound(f"Task {task_id} not found")

        old_status = task.status
        task_repo.complete().apply()
        task_dto = task.to_dto()

    producer = get_producer(EventTypes.BUSINESS_CALL)
    event = TaskCompletedEventSchema(
        data={
            "public_id": task.public_id,
            "old_status": old_status,
            "new_status": task.status,
        }
    )
    producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),
    )

    return task_dto
