**Чекер цены для binance биржи, в данном случае XPR/USDT**

Для запуска программы делаем следующие вещи:
1. `poetry install`(если не установлен, то устанавливаем через `pip install poetry`)
2. `celery -A tasks worker -B`(если не установлен redis, то устанавливаем [...](https://redis.io/docs/getting-started/installation/install-redis-on-linux/))
