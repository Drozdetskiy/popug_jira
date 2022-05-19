import enum


@enum.unique
class ProducerTypes(enum.Enum):
    BILLING_CYCLES_BC = "BILLING_CYCLES_BC"
    TASKCOSTS_BC = "TASKCOSTS_BC"
    TRANSACTIONS_BC = "TRANSACTIONS_BC"


REDIS_URL_TEMPLATE = "redis://{host}:{port}/{db}"
