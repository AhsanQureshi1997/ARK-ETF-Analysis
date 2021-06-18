import config
import alpaca_trade_api as tradeapi
import psycopg2

import psycopg2.extras

connection = psycopg2.connect(
    host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)

assets = api.list_assets()

print(len(assets))

for asset in assets:
    print(asset.name)
    print(asset.exchange)
    print(asset.symbol)

    cursor.execute("""
    INSERT INTO stock (name,symbol, exchange, is_etf)
    VALUES (%s, %s, %s, %s)
    """, (asset.name, asset.symbol, asset.exchange, False))


connection.commit()
