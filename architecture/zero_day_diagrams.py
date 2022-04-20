from functools import partial

from diagrams import (
    Diagram,
    Cluster,
    Node,
    Edge,
)
from diagrams.aws.compute import EC2
from diagrams.aws.database import (
    Database,
    ElasticacheCacheNode,
)
from diagrams.aws.general import Client
from diagrams.aws.integration import Eventbridge
from diagrams.aws.network import (
    APIGateway,
)
import enum

from diagrams.k8s.compute import Cronjob


class ExternalServices(enum.Enum):
    AUTH = "UberPopugIncAuth"
    WEB_CLIENT = "PopugJiraWebClient"
    GATEWAY = "PopugJiraGateway"


class InternalServices(enum.Enum):
    TASK_KEEPER = "TaskKeeper"
    ACCOUNT = "Account"
    ACCOUNTING = "Accounting"


SERVICE_TYPE_MAP = {
    ExternalServices.WEB_CLIENT: Client,
    ExternalServices.GATEWAY: APIGateway,
}


class EventBus(enum.Enum):
    TASK_EVENTS = "TaskEvents"
    REASSIGN_TASK_EVENTS = "ReassignTaskEvents"
    ACCOUNT_EVENTS = "AccountEvents"


def create_service(
        service: InternalServices | ExternalServices,
        storage: bool = False,
        cache: bool = False
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
        exclude: tuple[ExternalServices] = ()
) -> dict[ExternalServices, Node]:
    return {
        service_type: create_service(
            service_type,
        ) for service_type in ExternalServices if service_type not in exclude
    }


def create_event_buses() -> dict[EventBus, Node]:
    return {event_bus: create_event_bus(event_bus) for event_bus in EventBus}


def create_internal_services(
        exclude: tuple[InternalServices] = (),
        **kwargs
) -> dict[InternalServices, Node]:
    creator = partial(create_service, **kwargs)
    return {
        service: creator(
            service=service,
        ) for service in InternalServices if service not in exclude
    }


def draw_services_diagram(**kwargs):
    with Diagram("Services Diagram", **kwargs):
        external_services_map = create_external_services(
            exclude=(ExternalServices.GATEWAY, )
        )

        external_services_map[ExternalServices.AUTH]\
            << Edge(label="https")\
            << external_services_map[ExternalServices.WEB_CLIENT]

        with Cluster("Gateway"):
            gateway = create_service(ExternalServices.GATEWAY, cache=True)

        external_services_map[ExternalServices.WEB_CLIENT]\
            >> Edge(label="https")\
            >> gateway

        with Cluster("Services Under Gateway"):
            internal_services_map = create_internal_services(
                exclude=(InternalServices.ACCOUNTING, ),
                storage=True
            )
            with Cluster("Accounting"):
                accounting = create_service(
                    InternalServices.ACCOUNTING, storage=True
                )
                worker = Cronjob("BillingSendWorker")
                accounting - worker

            internal_services_map[InternalServices.ACCOUNTING] = accounting


        gateway >> Edge(label="http") >> list(internal_services_map.values())


def draw_eventsourcing_diagram(**kwargs):
    with Diagram("EventSourcing diagram", **kwargs):
        auth = create_service(ExternalServices.AUTH)
        account_bus = create_event_bus(EventBus.ACCOUNT_EVENTS)
        auth >> account_bus

        internal_services_map = create_internal_services()
        account_bus >> list(internal_services_map.values())
        task_bus = create_event_bus(EventBus.TASK_EVENTS)
        internal_services_map[InternalServices.TASK_KEEPER] >> task_bus
        task_reassign_bus = create_event_bus(EventBus.REASSIGN_TASK_EVENTS)
        internal_services_map[InternalServices.TASK_KEEPER] >> task_reassign_bus  # noqa
        task_reassign_bus >> internal_services_map[InternalServices.ACCOUNTING]
        task_bus >> internal_services_map[InternalServices.ACCOUNTING]


if __name__ == '__main__':
    draw_services_diagram(show=False, direction="TB")
    draw_eventsourcing_diagram(show=False)
