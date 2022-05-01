import enum
from functools import partial

from diagrams import (
    Diagram,
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


class Services(enum.Enum):
    AUTH = "UberPopugIncAuth"
    WEB_CLIENT = "PopugJiraWebClient"
    GATEWAY = "PopugJiraGateway"
    TASK_KEEPER = "TaskKeeper"
    ACCOUNT = "Account"
    ACCOUNTING = "Accounting"
    ANALYTICS = "Analytics"


SERVICE_TYPE_MAP = {
    Services.WEB_CLIENT: Client,
    Services.GATEWAY: APIGateway,
}


class EventBus(enum.Enum):
    TASK_EVENTS = "TaskEvents"
    REASSIGN_TASK_EVENTS = "ReassignTaskEvents"
    ACCOUNT_EVENTS = "AccountEvents"
    BillingEvents = "BillingEvents"


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


def create_external_services(
    exclude: tuple[Services] = (),
) -> dict[Services, Node]:
    return {
        service_type: create_service(service_type)
        for service_type in Services
        if service_type not in exclude
    }


def create_event_buses() -> dict[EventBus, Node]:
    return {event_bus: create_event_bus(event_bus) for event_bus in EventBus}


def create_internal_services(
    exclude: tuple[Services] = (), **kwargs
) -> dict[Services, Node]:
    creator = partial(create_service, **kwargs)
    return {
        service: creator(
            service=service,
        )
        for service in Services
        if service not in exclude
    }


def draw_gateway_diagram(**kwargs):
    with Diagram("Services gateway diagram", **kwargs):
        auth = create_service(Services.AUTH)
        analytics = create_service(Services.ANALYTICS)
        accounting = create_service(Services.ACCOUNTING)
        task_keeper = create_service(Services.TASK_KEEPER)
        client = create_service(Services.WEB_CLIENT)

        gateway = create_service(Services.GATEWAY)

        client >> gateway
        gateway >> auth
        client >> auth

        gateway >> analytics
        gateway >> accounting
        gateway >> task_keeper


def draw_gateway_events_diagram(**kwargs):
    with Diagram("Events gateway diagram", **kwargs):
        auth = create_service(Services.AUTH)
        analytics = create_service(Services.ANALYTICS)
        accounting = create_service(Services.ACCOUNTING)
        task_keeper = create_service(Services.TASK_KEEPER)

        account_bus = create_event_bus(EventBus.ACCOUNT_EVENTS)
        task_bus = create_event_bus(EventBus.TASK_EVENTS)
        billing_bus = create_event_bus(EventBus.BillingEvents)

        auth >> account_bus
        account_bus >> accounting
        account_bus >> task_keeper
        account_bus >> analytics

        task_keeper >> task_bus
        task_bus >> accounting
        task_bus >> analytics

        accounting >> billing_bus
        billing_bus >> analytics


if __name__ == "__main__":
    draw_gateway_diagram(show=False, direction="TB")
    draw_gateway_events_diagram(show=False)
