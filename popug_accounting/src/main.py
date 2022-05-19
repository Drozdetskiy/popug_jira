import os  # isort:skip

from conf import AMQPConfigSettings
from constants import ProducerTypes
from events.producers import init_producer

from popug_sdk.conf import settings

os.environ.setdefault("SETTINGS_MODULE", "src.conf")  # noqa

from api import api_router as v1_api_router
from fastapi import FastAPI

from popug_sdk.application import app

app.include_router(v1_api_router, prefix="/v1")


@app.on_event("startup")
def start_amqp() -> None:
    amqp_config: AMQPConfigSettings = settings.amqp
    init_producer(ProducerTypes.TASKCOSTS_BC, amqp_config.taskcosts_bc_amqp)
    init_producer(
        ProducerTypes.TRANSACTIONS_BC, amqp_config.transactions_bc_amqp
    )


def get_app() -> FastAPI:
    return app
