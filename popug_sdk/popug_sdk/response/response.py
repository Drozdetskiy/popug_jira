from typing import Any


def get_response_data(
    result: Any,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {"result": result, "meta": meta or {}}
