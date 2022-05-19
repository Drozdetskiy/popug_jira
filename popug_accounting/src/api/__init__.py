from api.v1.endpoints import (
    billing_cycle,
    hello_world,
)
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(
    hello_world.router, prefix="/hello-world", tags=["hello_world"]
)
api_router.include_router(
    billing_cycle.router,
    prefix="/billing_cycles",
    tags=["billing_cycles"],
)
