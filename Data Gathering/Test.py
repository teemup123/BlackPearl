from HistoricalOpenPrice import Get_1min_Candle
from SimpleStratAnalysis import simple_analysis

Symbol = 'BTCUSDT'
startDate = 'Jan 1, 2021'
endDate  = 'Mar 30, 2021'
file_name = 'Jan1-Mar30_1min.csv'

Get_1min_Candle(Symbol, startDate, endDate, file_name)

pEstLong = 0.5/100
pEstShort = 0.5/100
takeProf = 0.5/100
stopLoss = 0.5/100

simple_analysis(file_name,pEstLong,pEstShort,takeProf,stopLoss)