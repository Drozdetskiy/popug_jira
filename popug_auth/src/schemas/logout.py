from pydantic import BaseModel


class LogoutResponse(BaseModel):
    status: str
    username: str
