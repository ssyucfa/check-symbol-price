from celery import Celery

from services import get_xpr_price_change, get_xpr_prices, set_xpr

app = Celery("price_change")
app.conf.broker_url = "redis://localhost:6379/0"
app.conf.result_backend = "redis://localhost:6379/0"

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

    prices = get_xpr_prices()
    xpr_price_change = get_xpr_price_change(prices["cached_xpr_price"], prices["current_xpr_price"])

    if xpr_price_change >= 1:
        print("Цена снизилась на 1 процент или больше")

        set_xpr(prices["current_xpr_price"])

    print("Task finished")
