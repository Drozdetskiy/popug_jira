from fastapi import APIRouter
from src.schemas.hello_world import HelloWorldModel

__all__ = ("router",)


router = APIRouter()


@router.get(
    "/",
    name="Get hello world",
    response_model=HelloWorldModel,
)
def get_hello_world():
    """Simple hello world response"""
    return {
        "project": "popug_taskkeeper",
        "message": "Hello world!",
    }
