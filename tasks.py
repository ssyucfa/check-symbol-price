import os

from celery import Celery

import services

app = Celery("price_change")
app.conf.broker_url = os.getenv("redis://localhost:6379/0")
app.conf.result_backend = os.getenv("redis://localhost:6379/0")

app.conf.beat_schedule = {
    "check_price": {
        "task": "tasks.check_xpr_usdt_price",
        "schedule": 1.0,
    },
}
app.conf.timezone = "UTC"


@app.task
def check_xpr_usdt_price() -> None:
    print("Task started")

    services.check_xpr_usdt_price()

    print("Task finished")
