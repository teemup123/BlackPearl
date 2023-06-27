import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *
import numpy as np 

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_5m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'BTCUSDT'
TRADE_QUANTITY = 0.006

closes = []
dataarray = []
in_position = False


client = Client(config.API_KEY, config.API_SECRET)

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True
    
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_position, dataarray

    print('received message')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']
    is_candle_closed = candle['x']

    Open = candle['o']
    High = candle['h']
    Low = candle['l']
    Close = candle['c']
    Volume = candle['v']
    
    if is_candle_closed: 
        dataarray.append(float(Open))
        dataarray.append(float(High))
        dataarray.append(float(Low))
        dataarray.append(float(Close))
        dataarray.append(float(Volume))
    print('DataArrayPost:', dataarray)

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()