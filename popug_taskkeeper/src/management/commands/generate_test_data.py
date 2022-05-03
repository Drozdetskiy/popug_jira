from constants import UserRoles
from models import (
    Task,
    User,
)
from utils import get_public_id

from popug_sdk.db import create_session


def generate_test_data() -> None:
    for _ in range(10):
        with create_session() as session:
            user = User(
                public_id=get_public_id(),
                username="test_user",
                role=UserRoles.EMPLOYEE,
            )
            session.add(user)
            session.flush()
            task = Task(
                title="test_task",
                assignee_id=user.id,
                description="test_description",
            )
            session.add(task)
            session.commit()

    print("Done.")
