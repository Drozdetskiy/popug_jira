import os  # isort:skip

from constants import EventTypes
from events.user.producers import get_producer
from fastapi import FastAPI

os.environ.setdefault("SETTINGS_MODULE", "src.conf")  # noqa

from api import api_router as v1_api_router

from popug_sdk.application import app

app.include_router(v1_api_router, prefix="/v1")


@app.on_event("startup")
def start_amqp() -> None:
    user_bc_events_producer = get_producer(EventTypes.BUSINESS_CALL)
    user_ds_events_producer = get_producer(EventTypes.DATA_STREAMING)

    user_bc_events_producer.open_connection()
    user_ds_events_producer.open_connection()


def get_app() -> FastAPI:
    return app
