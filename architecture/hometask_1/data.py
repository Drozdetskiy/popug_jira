from diagrams import (
    Cluster,
    Diagram,
)
from diagrams.programming.flowchart import (
    InternalStorage,
    StoredData,
)


def draw_data_diagram(**kwargs):
    with Diagram("Data diagram", **kwargs):
        with Cluster("Auth"):
            with Cluster("User"):
                user = InternalStorage("User")
                name = StoredData("Name")
                email = StoredData("Email")
                role = StoredData("Role")

                name - user
                email - user
                role - user

        with Cluster("TaskKeeper"):
            user_for_task_keeper = InternalStorage("User (ReadOnly)")

            with Cluster("Task"):
                task = InternalStorage("Task")
                desc = StoredData("Description")
                assignee = StoredData("Assignee (User)")
                status = StoredData("Status")

                desc - task
                assignee - task
                status - task

            user_for_task_keeper - assignee

        user_for_task_keeper - user

        with Cluster("Accounting"):
            tasks_for_accounting = InternalStorage("Task (ReadOnly)")
            user_for_accounting = InternalStorage("User (ReadOnly)")

            with Cluster("Transaction"):
                transaction = InternalStorage("Transaction")
                owner = StoredData("Owner (User)")
                linked_task = StoredData("LinkedTask (Task, nullable)")
                bill = StoredData("Bill")
                type = StoredData("Type")

                owner - transaction
                linked_task - transaction
                bill - transaction
                type - transaction

            with Cluster("BillingCycle"):
                cycle = InternalStorage("BillingCycle")
                cycle_status = StoredData("Status")
                cycle - cycle_status

            owner - user_for_accounting
            transaction - cycle

            with Cluster("TaskCost"):
                task_cost = InternalStorage("TaskCost")
                costed_task = StoredData("CostedTask (Task)")
                debit_cost = StoredData("Debit cost")
                credit_cost = StoredData("Credit cost")

                debit_cost - task_cost
                credit_cost - task_cost
                costed_task - task_cost

            with Cluster("AccrueBillRequest"):
                accrue_bill_request = InternalStorage("AccrueBillRequest")
                status = StoredData("Status")
                requested_bill = StoredData("Bill")

                status - accrue_bill_request
                requested_bill - accrue_bill_request

            linked_task - tasks_for_accounting
            costed_task - tasks_for_accounting

        tasks_for_accounting - task
        user_for_accounting - user

        with Cluster("Analytics"):
            task_for_analytics = InternalStorage("Task (ReadOnly)")
            user_for_analytics = InternalStorage("User (ReadOnly)")
            transaction_for_analytics = InternalStorage(
                "Transaction (ReadOnly)"
            )
            task_cost_for_analytics = InternalStorage("TaskCost (ReadOnly)")
            cycle_for_analytics = InternalStorage("BillingCycle (ReadOnly)")

        task_for_analytics - task
        user_for_analytics - user
        transaction_for_analytics - transaction
        task_cost_for_analytics - task_cost
        cycle_for_analytics - cycle


if __name__ == "__main__":
    draw_data_diagram(show=False, direction="TB")
