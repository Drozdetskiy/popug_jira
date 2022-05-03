from api.v1.endpoints import (
    hello_world,
    tasks,
    users,
)
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(
    hello_world.router, prefix="/hello-world", tags=["hello_world"]
)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
