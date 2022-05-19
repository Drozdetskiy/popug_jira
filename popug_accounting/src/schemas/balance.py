from pydantic import BaseModel


class BalanceSchema(BaseModel):
    debit: int
    credit: int
    user_id: int
    billing_cycle_id: int
