import logging
from random import randint
from typing import Any

from popug_sdk.conf import settings

logger = logging.getLogger(settings.project)


def get_debit_cost() -> int:
    return randint(-20, -10)


def get_credit_cost() -> int:
    return randint(20, 40)


def send_email_notification(*args: Any, **kwargs: Any) -> None:
    logger.info("Mocked sending email notification")
