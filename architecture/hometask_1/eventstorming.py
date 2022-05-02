from diagrams import (
    Cluster,
    Diagram,
)
from diagrams.aws.business import Workmail
from diagrams.aws.general import User
from diagrams.aws.integration import EventResource
from diagrams.aws.iot import (
    IotAction,
    IotAnalyticsDataSet,
)

UNIT_TYPES_MAP = {
    "command": IotAction,
    "actor": User,
    "call": EventResource,
    "event": Workmail,
    "data": IotAnalyticsDataSet,
}


def draw_event_unit(event=None, **kwargs):
    with Cluster(kwargs["command"]):
        chain_map = {}

        for key, value in kwargs.items():
            unit = UNIT_TYPES_MAP[key]

            node = unit(value)
            chain_map[key] = node

        unit, *_chain = list(chain_map.values())

        for next_unit in _chain:
            unit >> next_unit
            unit = next_unit

    if isinstance(event, list):
        for i, e in enumerate(event):
            event_node = UNIT_TYPES_MAP["event"](e)
            if _chain:
                _chain[-1] >> event_node

            chain_map[f"event_{i}"] = event_node
    elif event:
        event_node = UNIT_TYPES_MAP["event"](event)

        if _chain:
            _chain[-1] >> event_node

        chain_map["event"] = event_node

    return chain_map


def draw_data_diagram(**kwargs):
    with Diagram("Eventstorming diagram", **kwargs):
        with Cluster("Auth"):
            draw_event_unit(
                actor="User(Any)",
                command="log_in",
                data="???",
                event="user.logged_in (BC)",
            )
            draw_event_unit(
                actor="User(Admin)",
                command="register_user",
                data="User(all fields)",
                event="user.registered (BC)",
            )
            get_user_by_pid = draw_event_unit(
                actor="User(Admin)",
                command="get_user_by_pid",
                data="User(pid +\nupdated fields)",
            )
            get_user_by_pid_data = get_user_by_pid["data"]

            grant_role_to_user = draw_event_unit(
                actor="User(Admin)",
                command="grant_role_to_user",
                data="User(updated fields)",
                event="user.role_granted (BC)",
            )
            grant_role_to_user_actor = grant_role_to_user["actor"]
            get_user_by_pid_data >> grant_role_to_user_actor

        with Cluster("TaskKeeper"):
            add_task = draw_event_unit(
                actor="User(Any)",
                command="add_task",
                data="Task(description)",
                event=["task.created (DS)", "task.assigned (BC)"],
            )
            create_task_event = add_task["event_0"]
            assign_task_event = add_task["event_1"]

            shuffle_task = draw_event_unit(
                actor="User(Manager/Admin)",
                command="shuffle_task",
                data="Task(by open status),\nUser(employee)",
            )
            shuffle_task_data = shuffle_task["data"]
            shuffle_task_data >> assign_task_event
            get_task_by_assignee = draw_event_unit(
                actor="User(Any)",
                command="get_task_by_assignee",
                data="Task(all fields),\nUser(employee)",
            )
            get_task_by_assignee_data = get_task_by_assignee["data"]
            complete_task = draw_event_unit(
                actor="User(Any)",
                command="complete_task",
                data="Task(by pid)",
                event="task.completed (BC)",
            )
            complete_task_event = complete_task["event"]
            complete_task_actor = complete_task["actor"]
            get_task_by_assignee_data >> complete_task_actor

        with Cluster("Accounting"):
            add_task_cost = draw_event_unit(
                command="add_task_cost",
                data="Task(pid)",
                event="task_cost.added (BC)",
            )
            add_task_cost_command = add_task_cost["command"]
            create_task_event >> add_task_cost_command
            draw_event_unit(
                actor="User(Any)",
                command="get_balance",
                data="Transaction\n(count BL\nby user & by datetime)",
            )
            close_billing_cycle = draw_event_unit(
                call="CronTask",
                command="CloseBillingCycle",
                data="Transaction\n(count BL)",
                event=[
                    "billing_cycle.closed\n(BC)",
                    "payed_transaction.applied\n(BC)",
                ],
            )
            payed_transaction_event = close_billing_cycle["event_1"]
            pay_money = draw_event_unit(
                command="pay_money",
                data="Transaction\n(count BL\nby user & by cycle)",
                event="billing_cycle.payed (BC)",
            )
            payed_transaction_event >> pay_money["command"]
            debit_bill = draw_event_unit(
                command="debit_bill",
                data="TaskCost(debit_cost)",
                event="Transaction.added (BC)",
            )
            transaction_event = debit_bill["event"]
            debit_billing_command = debit_bill["command"]
            assign_task_event >> debit_billing_command
            credit_bill = draw_event_unit(
                command="credit_bill",
                data="Task(credit_cost)",
            )
            credit_billing_command = credit_bill["command"]
            credit_billing_data = credit_bill["data"]
            complete_task_event >> credit_billing_command
            credit_billing_data >> transaction_event


if __name__ == "__main__":
    draw_data_diagram(show=False)
