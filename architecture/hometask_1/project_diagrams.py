import enum

from diagrams import (
    Cluster,
    Diagram,
    Edge,
    Node,
)
from diagrams.aws.compute import EC2
from diagrams.aws.database import (
    Database,
    ElasticacheCacheNode,
)
from diagrams.aws.general import Client
from diagrams.aws.integration import Eventbridge
from diagrams.aws.network import APIGateway
from diagrams.k8s.compute import Cronjob


class Services(enum.Enum):
    AUTH = "Auth"
    WEB_CLIENT = "PopugJiraWebClient"
    TASK_KEEPER = "TaskKeeper"
    ACCOUNTING = "Accounting"
    ANALYTICS = "Analytics"
    GATEWAY = "Gateway"


SERVICE_TYPE_MAP = {
    Services.WEB_CLIENT: Client,
    Services.GATEWAY: APIGateway,
}


class EventBus(enum.Enum):
    TASK_EVENTS = "TaskEvents"
    REASSIGN_TASK_EVENTS = "ReassignTaskEvents"
    ACCOUNT_EVENTS = "AccountEvents"
    TRANSACTION_EVENTS = "TransactionEvents"
    TASK_COST_EVENTS = "TaskCostEvents"
    BILLING_CYCLE_EVENTS = "BillingCycleEvents"


def create_service(
    service: Services,
    storage: bool = False,
    cache: bool = False,
) -> Node:
    node = SERVICE_TYPE_MAP.get(service, EC2)(service.value)

    if storage:
        service_storage = Database(f"{service.value}Storage")
        node - service_storage

    if cache:
        service_cache = ElasticacheCacheNode(f"{service.value}Cache")
        node - service_cache

    return node


def create_event_bus(event_bus: EventBus) -> Node:
    return Eventbridge(event_bus.value)


def draw_gateway_diagram(**kwargs):
    with Diagram("Services diagram", **kwargs):
        with Cluster("Gateway"):
            gateway = create_service(Services.GATEWAY, cache=True)
        with Cluster("Auth"):
            auth = create_service(Services.AUTH, storage=True)

        with Cluster("PrivateNetwork"):
            with Cluster("Analytics"):
                analytics = create_service(Services.ANALYTICS, storage=True)

            with Cluster("Accounting"):
                accounting = create_service(Services.ACCOUNTING, storage=True)
                worker = Cronjob("BillingSendWorker")
                accounting - worker

            with Cluster("TaskKeeper"):
                task_keeper = create_service(
                    Services.TASK_KEEPER, storage=True
                )
                worker = Cronjob("ReassignWorker")
                task_keeper - worker

        client = create_service(Services.WEB_CLIENT)

        client >> Edge(label="https") >> auth
        client >> Edge(label="https") >> gateway
        auth >> Edge(label="https") >> gateway

        gateway >> Edge(label="http") >> analytics
        gateway >> Edge(label="http") >> accounting
        gateway >> Edge(label="http") >> task_keeper


def draw_gateway_events_diagram(**kwargs):
    with Diagram("Events diagram", **kwargs):
        auth = create_service(Services.AUTH)
        analytics = create_service(Services.ANALYTICS)

        accounting = create_service(Services.ACCOUNTING)
        task_keeper = create_service(Services.TASK_KEEPER)

        account_bus = create_event_bus(EventBus.ACCOUNT_EVENTS)
        task_bus = create_event_bus(EventBus.TASK_EVENTS)
        transaction_bus = create_event_bus(EventBus.TRANSACTION_EVENTS)
        billing_cycle_bus = create_event_bus(EventBus.BILLING_CYCLE_EVENTS)
        task_cost_bus = create_event_bus(EventBus.TASK_COST_EVENTS)

        auth >> account_bus
        account_bus >> accounting
        account_bus >> task_keeper
        account_bus >> analytics

        task_keeper >> task_bus
        accounting >> task_cost_bus
        task_bus >> accounting
        task_bus >> analytics
        task_cost_bus >> analytics

        accounting >> transaction_bus >> analytics
        accounting >> billing_cycle_bus >> analytics


if __name__ == "__main__":
    draw_gateway_diagram(show=False, direction="TB")
    draw_gateway_events_diagram(show=False)
