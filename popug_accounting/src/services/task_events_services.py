import json
import logging
from functools import singledispatch

from events.task.events_map import TASK_EVENTS_MAP
from events.taskcost.send_event import send_taskcost_added_event
from events.transaction.send_event import send_transaction_added_event
from events.utils import event_data_fabric
from pydantic import BaseModel
from repos.billing_cycle import BillingCycleRepo
from repos.task import TaskRepo
from repos.taskcost import TaskCostRepo
from repos.transaction import TransactionRepo
from repos.user import UserRepo

from popug_schema_registry.models.v1.task_assigned_event_schema import (
    TaskAssignedEventSchema,
)
from popug_schema_registry.models.v1.task_completed_event_schema import (
    TaskCompletedEventSchema,
)
from popug_schema_registry.models.v1.task_created_event_schema import (
    TaskCreatedEventSchema,
)
from popug_schema_registry.models.v1.transaction_added_event_schema import (
    TransactionTypes,
)
from popug_sdk.conf import settings
from popug_sdk.db import create_session

logger = logging.getLogger(settings.project)


@singledispatch
def _process_event(event: BaseModel) -> None:
    raise NotImplementedError


@_process_event.register
def _complete_task(event: TaskCompletedEventSchema) -> None:
    taskcost_added = False

    with create_session() as session:
        billing_cycle = BillingCycleRepo(session).get_last(lock=True).get()
        task = TaskRepo(session).create_or_update(event.data.public_id).get()
        user = (
            UserRepo(session)
            .create_or_update(event.data.assignee_public_id)
            .get()
        )

        taskcost_repo = TaskCostRepo(session)
        taskcost = taskcost_repo.get_by_task_id(task.id).context()

        if not taskcost:
            taskcost = taskcost_repo.add(task.id).get()
            taskcost_added = True

        transaction = (
            TransactionRepo(session)
            .add(
                credit=taskcost.credit_cost,
                task_id=task.id,
                user_id=user.id,
                billing_cycle_id=billing_cycle.id,
                type=TransactionTypes.INCOME,
            )
            .apply()
        )
        transaction_dto = transaction.to_dto()
        logger.info(
            f"{task = } completed with {taskcost = } by {user = }. "
            f"{transaction_dto = } added."
        )

    if taskcost_added:
        send_taskcost_added_event(taskcost, task)

    send_transaction_added_event(transaction_dto)


@_process_event.register
def _assign_task(event: TaskAssignedEventSchema) -> None:
    taskcost_added = False

    with create_session() as session:
        billing_cycle = BillingCycleRepo(session).get_last(lock=True).get()
        task = TaskRepo(session).create_or_update(event.data.public_id).get()
        user = (
            UserRepo(session)
            .create_or_update(event.data.new_assignee_public_id)
            .get()
        )
        taskcost_repo = TaskCostRepo(session)
        taskcost = taskcost_repo.get_by_task_id(task.id).context()

        if not taskcost:
            taskcost = taskcost_repo.add(task.id).get()
            taskcost_added = True

        transaction = (
            TransactionRepo(session)
            .add(
                debit=taskcost.debit_cost,
                task_id=task.id,
                user_id=user.id,
                billing_cycle_id=billing_cycle.id,
                type=TransactionTypes.EXPENSE,
            )
            .apply()
        )
        transaction_dto = transaction.to_dto()
        logger.info(
            f"{task = } assigned with {taskcost = } to {user = }. "
            f"{transaction_dto = } added."
        )

    if taskcost_added:
        send_taskcost_added_event(taskcost, task)

    send_transaction_added_event(transaction_dto)


@_process_event.register
def _create_task(event: TaskCreatedEventSchema) -> None:
    taskcost_added = False

    with create_session() as session:
        data = event.data.dict()
        public_id = data.pop("public_id")
        task = TaskRepo(session).create_or_update(public_id, **data).get()
        taskcost_repo = TaskCostRepo(session)
        taskcost = taskcost_repo.get_by_task_id(task.id).context()

        if not taskcost:
            taskcost = taskcost_repo.add(task.id).apply()
            taskcost_added = True

        logger.info(f"{task = } created with {taskcost = }.")

    if taskcost_added:
        send_taskcost_added_event(taskcost, task)


def process_task_event_message(message: bytes) -> None:
    event = event_data_fabric(json.loads(message), TASK_EVENTS_MAP)
    logger.info(f"Processing event: {event}")
    _process_event(event)
