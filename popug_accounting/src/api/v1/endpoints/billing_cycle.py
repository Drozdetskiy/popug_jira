from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from repos.exceptions import BillingCycleNotFound
from schemas.balance import BalanceSchema
from schemas.billing_cycle import BillingCycleSchema
from schemas.meta import BalanceResponseMetaSchema
from services.balances import (
    count_balances as count_balances_service,
    get_balances as get_balances_service,
)
from services.billing_cycles import (
    count_billing_cycles as count_billing_cycles_service,
    get_billing_cycle as get_billing_cycle_service,
    get_billing_cycles as get_billing_cycles_service,
)
from starlette import status

from popug_sdk.dependencies.pagination import PagePagination
from popug_sdk.response.response import get_response_data
from popug_sdk.schemas.response_schema import (
    get_list_response_schema,
    get_response_schema,
)

__all__ = ("router",)


router = APIRouter()


@router.get(
    "/{billing_cycle_id}",
    response_model=get_response_schema(BillingCycleSchema, suffix="Detail"),
)
def get_billing_cycle(billing_cycle_id: int) -> dict[str, Any]:
    try:
        billing_cycle = get_billing_cycle_service(billing_cycle_id)
    except BillingCycleNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return get_response_data(billing_cycle)


@router.get(
    "/",
    response_model=get_list_response_schema(BillingCycleSchema),
)
def get_billing_cycles(
    pagination: PagePagination = Depends(PagePagination),
) -> dict[str, Any]:
    billing_cycles = get_billing_cycles_service(
        limit=pagination.limit,
        offset=pagination.offset,
    )
    count = count_billing_cycles_service()

    return get_response_data(billing_cycles, meta=pagination.get_params(count))


@router.get(
    "/{billing_cycle_id}/balances",
    response_model=get_list_response_schema(
        BalanceSchema, meta_schema=BalanceResponseMetaSchema
    ),
)
def get_balances(
    billing_cycle_id: int,
    pagination: PagePagination = Depends(PagePagination),
    user_id: int | None = Query(None),
) -> dict[str, Any]:
    count = count_balances_service(billing_cycle_id, user_id)

    return get_response_data(
        get_balances_service(
            billing_cycle_id, user_id, pagination.limit, pagination.offset
        ),
        meta=pagination.get_params(count),
    )
