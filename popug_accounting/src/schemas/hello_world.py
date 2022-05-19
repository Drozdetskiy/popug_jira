from pydantic import BaseModel


class HelloWorldModel(BaseModel):
    project: str
    message: str
