from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TaskDTO:
    id: int
    public_id: str
    title: str
    description: str

    @classmethod
    def get_dto_from_dict(cls, **data: Any) -> TaskDTO:
        id_ = data["id"]
        public_id = data["public_id"]
        description = data["description"]

        jira_id = data.get("jira_id")

        if jira_id is not None:
            title = f"{jira_id} - {data['short_title']}"
        else:
            title = data["title"]

        return cls(
            id=id_, public_id=public_id, title=title, description=description
        )
