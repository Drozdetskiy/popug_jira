from api.v1.endpoints import hello_world
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(
    hello_world.router, prefix="/hello-world", tags=["hello_world"]
)
