from typing import Any

from fastapi import APIRouter
from schemas.hello_world import HelloWorldModel

__all__ = ("router",)


router = APIRouter()


@router.get(
    "/",
    name="Get hello world",
    response_model=HelloWorldModel,
)
def get_hello_world() -> dict[str, Any]:
    """Simple hello world response"""
    return {
        "project": "popug_accounting",
        "message": "Hello world!",
    }
