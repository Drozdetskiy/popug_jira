from pydantic import BaseModel


class Pong(BaseModel):
    project: str
    version: str
    datetime: str
