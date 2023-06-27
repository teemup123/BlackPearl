#This function takes in 1. Symbol 2. Candle Time 3. Date Range
    #enter startDate and endDate as string in this format "1 Jan, 2018"E
    # Returns 1. Historical CSV file 

def  Get_30min_Candle(Symbol, startDate, endDate, file_name):

    import config, csv
    from binance.client import Client

    client = Client(config.API_KEY, config.API_SECRET)

    csvfile = open(file_name, 'w', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')
    candlesticks = client.get_historical_klines(Symbol , client.KLINE_INTERVAL_30MINUTE, startDate, endDate)

    for i in candlesticks:
        candlestick_writer.writerow(i)

    csvfile.close()
    return(candlesticks)

def  Get_5min_Candle(Symbol, startDate, endDate, file_name):

    import config, csv
    from binance.client import Client

    client = Client(config.API_KEY, config.API_SECRET)

    csvfile = open(file_name, 'w', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')
    candlesticks = client.get_historical_klines(Symbol , client.KLINE_INTERVAL_5MINUTE, startDate, endDate)

    for i in candlesticks:
        candlestick_writer.writerow(i)

    csvfile.close()
    return(candlesticks)

def  Get_1min_Candle(Symbol, startDate, endDate, file_name):

    import config, csv
    from binance.client import Client

    client = Client(config.API_KEY, config.API_SECRET)

    csvfile = open(file_name, 'w', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')
    candlesticks = client.get_historical_klines(Symbol , client.KLINE_INTERVAL_1MINUTE, startDate, endDate)

    for i in candlesticks:
        candlestick_writer.writerow(i)

    csvfile.close()
    return(candlesticks)



