from celery_app import app


@app.task
def process_cycle() -> None:
    from src.services.process_cycle import (
        process_cycle as process_cycle_service,
    )

    process_cycle_service()


@app.task
def close_cycle() -> None:
    from src.services.close_cycle import close_cycle as close_cycle_service

    close_cycle_service()


@app.task
def send_payment(user_id: int, billing_cycle_id: int) -> None:
    from src.services.sent_payment import sent_payment as sent_payment_service

    sent_payment_service(user_id, billing_cycle_id)


@app.task
def refresh_balance() -> None:
    from src.services.refresh_balance import (
        refresh_balance as refresh_balance_service,
    )

    refresh_balance_service()
