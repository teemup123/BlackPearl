import config
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)
candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_5MINUTE)
#print(candles[-1])
