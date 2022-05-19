from dataclasses import dataclass


@dataclass
class TaskDTO:
    id: int
    public_id: str
    title: str
    description: str
