from schemas.user import UserAddSchema
from services.users import add_user


def generate_test_user() -> None:
    user_data = UserAddSchema(
        username="test_user",
        email="test@test.com",
        beak_shape="beak_shape_for_test",
        role="ADMIN",
    )
    user = add_user(user_data)

    print(f"{user = }")
    print("Done.")
