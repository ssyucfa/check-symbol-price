**Чекер цены для binance биржи за последний час, в данном случае XPR/USDT**

Для запуска программы есть два варианта.

Первый:
1. `poetry install`(если не установлен, то устанавливаем через `pip install poetry`)
2. `celery -A tasks worker -B`(если не установлен redis, то устанавливаем [...](https://redis.io/docs/getting-started/installation/install-redis-on-linux/))

Второй:
1. `docker-compose up --build`(если не установлен докер и докер-композ, то установите)
