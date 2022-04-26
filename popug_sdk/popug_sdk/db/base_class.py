from typing import Any

from sqlalchemy.ext.declarative import (
    as_declarative,
    declared_attr,
)

__all__ = ("BaseModel",)


@as_declarative()
class BaseModel:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
