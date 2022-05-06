from pydantic import BaseModel


class AuthSettings(BaseModel):
    public_key: str = "public_key"
    algorithm: str = "RS256"
