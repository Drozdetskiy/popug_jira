import os  # isort:skip
import sys

os.environ.setdefault("SETTINGS_MODULE", "src.conf")  # noqa
sys.path.append(os.path.dirname(__file__))  # noqa

from celery import Celery
from conf import (
    AMQPConfigSettings,
    RedisConfigSettings,
)
from constants import (
    REDIS_URL_TEMPLATE,
    ProducerTypes,
)
from events.producers import init_producer
from schedules import (
    CLOSE_CYCLE_SCHEDULE,
    PROCESS_CYCLE_SCHEDULE,
    REFRESH_BALANCE_SCHEDULE,
)

from popug_sdk.conf import settings
from popug_sdk.db import init_db

app = Celery("popug_accounting")

DEFAULT_TASK_QUEUE = "default"
BASE_PATH = "src.tasks.{}"

TASK_ROUTES = {
    BASE_PATH.format("send_payment"): {
        "queue": "send_payment",
    }
}


SCHEDULE = {
    "process_cycle": {
        "task": BASE_PATH.format("process_cycle"),
        "schedule": PROCESS_CYCLE_SCHEDULE,
        "args": [],
        "kwargs": {},
    },
    "close_cycle": {
        "task": BASE_PATH.format("close_cycle"),
        "schedule": CLOSE_CYCLE_SCHEDULE,
        "args": [],
        "kwargs": {},
    },
    "refresh_balance": {
        "task": BASE_PATH.format("refresh_balance"),
        "schedule": REFRESH_BALANCE_SCHEDULE,
        "args": [],
        "kwargs": {},
    },
}


redis_config: RedisConfigSettings = settings.redis
app.conf.update(
    broker_url=REDIS_URL_TEMPLATE.format(
        host=redis_config.celery_broker.host,
        port=redis_config.celery_broker.port,
        db=redis_config.celery_broker.db,
    ),
    result_backend=REDIS_URL_TEMPLATE.format(
        host=redis_config.celery_result.host,
        port=redis_config.celery_result.port,
        db=redis_config.celery_result.db,
    ),
    beat_schedule=SCHEDULE,
    task_default_queue=DEFAULT_TASK_QUEUE,
    task_routes=TASK_ROUTES,
)
init_db()
amqp_config: AMQPConfigSettings = settings.amqp
init_producer(
    ProducerTypes.BILLING_CYCLES_BC, amqp_config.billing_cycles_bc_amqp
)
init_producer(ProducerTypes.TRANSACTIONS_BC, amqp_config.transactions_bc_amqp)

app.autodiscover_tasks(["src"])
