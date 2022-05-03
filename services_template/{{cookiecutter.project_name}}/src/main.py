import os  # isort:skip

os.environ.setdefault("SETTINGS_MODULE", "src.conf")  # noqa

from fastapi import FastAPI
from src.api import api_router as v1_api_router

from popug_sdk.application import app

app.include_router(v1_api_router, prefix="/v1")


def get_app() -> FastAPI:
    return app
