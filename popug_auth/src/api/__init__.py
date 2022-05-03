from api.v1.endpoints import (
    hello_world,
    oauth,
    users,
)
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(
    hello_world.router, prefix="/hello-world", tags=["hello_world"]
)
api_router.include_router(oauth.router, prefix="/oauth", tags=["oauth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
