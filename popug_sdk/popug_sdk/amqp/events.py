import uuid
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)


class BaseEvent(BaseModel):
    pid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
