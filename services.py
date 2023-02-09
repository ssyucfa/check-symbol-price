import decimal
import os
from datetime import datetime, timedelta
from typing import Any

import redis
import requests

SYMBOL = "XRPUSDT"
BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")


def get_redis_connection() -> redis.Redis:
    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    return r


def _get_xpr_price() -> decimal.Decimal:
    data = requests.get(BINANCE_PRICE_URL, params={"symbol": SYMBOL}).json()
    return decimal.Decimal(data["price"])


def set_xpr(current_xpr_price: decimal.Decimal, r: redis.Redis = get_redis_connection()):
    r.set("xpr_set_time", str(datetime.now()))
    r.set("xpr_price", float(current_xpr_price))


def get_xpr_prices() -> dict[str, Any]:
    r = get_redis_connection()

    last_cache_time = r.get("xpr_set_time")
    cached_xpr_price = r.get("xpr_price")
    current_xpr_price = round(_get_xpr_price(), 6)

    if last_cache_time is None or datetime.fromisoformat(last_cache_time.decode()) < datetime.now() - timedelta(hours=1):
        set_xpr(current_xpr_price, r)

    return {
        "cached_xpr_price": round(decimal.Decimal(cached_xpr_price.decode()), 6)
        if cached_xpr_price is not None
        else current_xpr_price,
        "current_xpr_price": current_xpr_price
    }


def get_xpr_price_change(cached_xpr_price: decimal.Decimal, current_xpr_price: decimal.Decimal):
    return round((cached_xpr_price - current_xpr_price) / cached_xpr_price * 100, 3)


def check_xpr_usdt_price() -> None:
    prices = get_xpr_prices()
    xpr_price_change = get_xpr_price_change(prices["cached_xpr_price"], prices["current_xpr_price"])

    # По тз было непонятно, нужно == или >=, так что выбрал наиболее логичное
    if xpr_price_change >= 1:
        print("Цена снизилась на 1 процент или больше")

        # По тз было непонятно, нужно ли менять значение, так что выбрал наиболее логичное
        set_xpr(prices["current_xpr_price"])
