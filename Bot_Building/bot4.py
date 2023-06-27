"""
Bot number 4 will properly display:
    1. Position status 
        a. bought status
        b. IF bought status is true:
            i. bought time 
            ii. bought price 
            iii. inst. returns 
            iv. time elapse
    2. General market/bot status
        a. Asset pair price
        b. last decision made
        c. on going decision
        d. Buy decision @ 
        e. Sell decision @
        f. bot name 
    3. General status of the code
        a. Internet connection to Binance
"""
import websocket, json
import config
from binance.client import Client
from binance.enums import *
import numpy as np
from sklearn.preprocessing import StandardScaler
import keras
import urllib.request
import pandas as pd
import datetime
import talib
     
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1h"
TRADE_SYMBOL = 'BTCUSDT'
ML_model_name = 'CNNModel5.01'
model = keras.models.load_model(ML_model_name)
client = Client(config.API_KEY, config.API_SECRET)

class positionInfo: 
    def __init__(self): 

        self.in_position = False
        self.candle_since_bought = []
        self.unix_bought_time = 'N/A'
        self.bought_price = 'N/A'
        self.currentprice = 'this will just be mapped to outside once the position is taken'

    def generate_position_status(self):
        if self.in_position == False: 
            print('Not in position')
        else:
            print('In position:', self.in_position)

            self.readable_bought_time = int(self.unix_bought_time) #convert unix date time to readable date time
            print(
                'Bought on: {}'.format(self.readable_bought_time)
            )

            print(
                'Hours sinced bought: {}'.format(
                    len(self.candle_since_bought)
                    )
                )

            print(
                'Bought at: {} USD'.format(self.bought_price)
            )    

            self.position_pl = float(self.currentprice)/float(self.bought_price)
            print('Current / BoughtPrice = {}'.format(self.position_pl))

class botStat:
    def __init__(self): 
        self.inst_decision = 'No Decision Defined'
        self.decision_made = 'No Decision Defined'
        self.hourly_array = 'no Data Array Defined'
        self.daily_array = 'N/A'
        self.weekly_array = 'N/A'
        self.technical_array = 'N/A'
        self.ref_time = 'Not yet defined'

        self.inst_hourly_array = 'no Data Array Defined'
        self.inst_daily_array = 'N/A'
        self.inst_weekly_array = 'N/A'
        self.inst_technical_array = 'N/A'

def order(side, quantity, symbol, price):
   try: 
       print("Sending Order")
       order = client.order_limit(symbol=symbol, side=side, quantity=quantity, price=str(price) )
       print(order)
   except Exception as e:
       print("an exception occured - {}".format(e))
       return False
 
   return True

def dataArray_parse(dataArray):
    hourly_data = dataArray[0:(34*5)].reshape(34,5)
    daily_data = dataArray[(34*5):((34*5)+(10*5))].reshape(10,5)
    weekly_data = dataArray[((34*5)+(10*5)):((34+10+2)*5)].reshape(2,5)
    technical_data = dataArray[((34+10+2)*5):].reshape(1,6)

    return(hourly_data, daily_data, weekly_data, technical_data)

def trunc(values, decs=0):
    return np.trunc(values*10**decs)/(10**decs)

def talib_calc(sample_close_array):
    (macd, macdsignal, macdhist) = talib.MACD(sample_close_array,  fastperiod=12, slowperiod=26, signalperiod=9)
    RSI = talib.RSI(sample_close_array, timeperiod=14)
    MA_Type = talib.MA_Type
    BBup, BBmid, BBlow = talib.BBANDS(sample_close_array, matype=MA_Type.T3)
    return(macd, macdsignal, RSI, BBup, BBmid, BBlow)

def gen_data():

    past_34_hour_klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR)
    past_10_days_kline = client.get_klines(symbol = 'BTCUSDT', interval = Client.KLINE_INTERVAL_1DAY)
    past_2_weeks_kline = client.get_klines(symbol = 'BTCUSDT', interval = Client.KLINE_INTERVAL_1WEEK)
    Data = []
    sample_close_array = np.array([])
    date = []

    for index, data in reversed(list(enumerate(past_34_hour_klines))):

        if index == len(past_34_hour_klines)-1: #Neglect the current on going candle
            continue

        date.append(data[0])

        Data.append(
            float(data[1])
        )
        
        Data.append(
            float(data[2])
        )
        
        Data.append(
            float(data[3])
        )
        
        Data.append(
            float(data[4])
        )
        
        Data.append(
            float(data[5])
        )
        
        if len(Data) == 34*5: 
            break 

    sample_close_array = np.array(Data)
    
    for index, data in reversed(list(enumerate(past_10_days_kline))):

        if index == len(past_10_days_kline)-1: #Neglect the current on going candle
            continue
        
        Data.append(
            float(data[1])
            )
        Data.append(
            float(data[2])
            )
        Data.append(
            float(data[3])
            )
        Data.append(
            float(data[4])
            )
        Data.append(
            float(data[5])
            )
        
        if len(Data) == 34*5 + 10*5: 
            break
    
    for index, data in reversed(list(enumerate(past_2_weeks_kline))):

        if index == len(past_2_weeks_kline)-1: #Neglect the current on going candle
            continue
        
        Data.append(
            float(data[1])
            )
        Data.append(
            float(data[2])
            )
        Data.append(
            float(data[3])
            )
        Data.append(
            float(data[4])
            )
        Data.append(
            float(data[5])
            )
        
        if len(Data) == (34 + 10 + 2)*5: 
            break

    (macd, macdsignal, RSI, BBup, BBmid, BBlow) = talib_calc(sample_close_array)

    Data.append(float(macd[-1]))
    Data.append(float(macdsignal[-1]))
    Data.append(float(RSI[-1]))
    Data.append(float(BBup[-1]))
    Data.append(float(BBmid[-1]))
    Data.append(float(BBlow[-1]))

    return Data, date

def gen_inst_data(ohlc_array):

    past_34_hour_klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR)
    past_10_days_kline = client.get_klines(symbol = 'BTCUSDT', interval = Client.KLINE_INTERVAL_1DAY)
    past_2_weeks_kline = client.get_klines(symbol = 'BTCUSDT', interval = Client.KLINE_INTERVAL_1WEEK)
    Data = []
    date = []

    for value in ohlc_array: 
        Data.append(value)

    for index, data in reversed(list(enumerate(past_34_hour_klines))):

        if index == len(past_34_hour_klines)-1: #Neglect the current on going candle
            continue

        Data.append(
            float(data[1])
        )
        
        Data.append(
            float(data[2])
        )
        
        Data.append(
            float(data[3])
        )
        
        Data.append(
            float(data[4])
        )
        
        Data.append(
            float(data[5])
        )
        
        if len(Data) == (34-1)*5: 
            break 
      
    sample_close_array = np.array(Data)

    for index, data in reversed(list(enumerate(past_10_days_kline))):

        if index == len(past_10_days_kline)-1: #Neglect the current on going candle
            continue
        
        Data.append(
            float(data[1])
            )
        Data.append(
            float(data[2])
            )
        Data.append(
            float(data[3])
            )
        Data.append(
            float(data[4])
            )
        Data.append(
            float(data[5])
            )
        
        if len(Data) == 34*5 + 10*5: 
            break
    
    for index, data in reversed(list(enumerate(past_2_weeks_kline))):

        if index == len(past_2_weeks_kline)-1: #Neglect the current on going candle
            continue
        
        Data.append(
            float(data[1])
            )
        Data.append(
            float(data[2])
            )
        Data.append(
            float(data[3])
            )
        Data.append(
            float(data[4])
            )
        Data.append(
            float(data[5])
            )
        
        if len(Data) == (34 + 10 + 2)*5: 
            break

    (macd, macdsignal, RSI, BBup, BBmid, BBlow) = talib_calc(sample_close_array)

    Data.append(float(macd[-1]))
    Data.append(float(macdsignal[-1]))
    Data.append(float(RSI[-1]))
    Data.append(float(BBup[-1]))
    Data.append(float(BBmid[-1]))
    Data.append(float(BBlow[-1]))
    inst_data = Data
    return inst_data
    
def on_open(ws): 
   print('opened connection')
 
def on_close(ws):  
   print('closed connection')

def on_message(ws, message):
    print('received message')

    json_message = json.loads(message)
    candle = json_message['k']
    time = int(json_message['E'])
    is_candle_closed = candle['x']   
    
    Open = float(candle['o'])
    High = float(candle['h'])
    Low = float(candle['l'])
    Close = float(candle['c'])
    Volume = float(candle['v'])
    ohlc_array = np.array([Open, High, Low, Close, Volume])

    inst_data = gen_inst_data(ohlc_array)
    inst_data = np.array(inst_data)
    (bot_stat.inst_hourly_array, bot_stat.inst_daily_array, bot_stat.inst_weekly_array, bot_stat.inst_technical_array) = dataArray_parse(inst_data) 
    dataArray = StandardScaler().fit_transform(inst_data.reshape(-1,1))
    inst_Prob = model.predict(
        np.array([dataArray.reshape(-1)])
        )
    
    bot_stat.inst_decision = inst_Prob[0][2]

    if is_candle_closed:

        data, date = gen_data()
        while (date/1000) < bot_stat.ref_time+(3600*2): #Incase binance updates the stream and the getkline differently
            data, date = gen_data()

        data = np.array(data)
        bot_stat.ref_time = date/1000
        (bot_stat.hourly_array, bot_stat.daily_array, bot_stat.weekly_array, bot_stat.technical_array) = dataArray_parse(data) 
        dataArray = StandardScaler().fit_transform(data.reshape(-1,1))
        Prob = model.predict(
            np.array([dataArray.reshape(-1)])
            )
        bot_stat.decision_made = Prob[2]
    
    
    print(bot_stat.inst_decision)

bot_stat = botStat()
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()