import enum


@enum.unique
class EventTypes(enum.Enum):
    BUSINESS_CALL = "BUSINESS_CALL"
    DATA_STREAMING = "DATA_STREAMING"
