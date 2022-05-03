from contextlib import suppress

from schemas.user import UserAddSchema
from services.exceptions import UserAlreadyExists
from services.users import create_user


def generate_test_user() -> None:
    user_data = UserAddSchema(
        username="test_user",
        email="test@test.com",
        beak_shape="beak_shape_for_test",
        role="ADMIN",
    )
    with suppress(UserAlreadyExists):
        user = create_user(user_data)
        print(f"{user = }")

    print("Done.")
