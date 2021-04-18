import websocket, json, pprint, binance, requests, pandas, datetime, talib, numpy
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import API_CREDENTIALS as cred
from binance.client import Client
from binance.enums import *
from functools import partial

BULLISH = 1
HOLD = 0
BEARISH = -1

SOCKET = "wss://stream.binance.com/ws/"
HTTP_ROOT = 'https://api.binance.com/api/v1/'
SYMBOL = "BTCUSDT"
STREAM = "@kline_"
PERIOD = "1m"
URL =  SOCKET + SYMBOL + STREAM + PERIOD

class Bot:
    def __init__(self, symbol1, symbol2, period, amount, indicators):
        self.indicators = indicators
        self.symbol = symbol1 + symbol2
        print(self.symbol)
        self.inPosition = False
        self.period = "1m"
        self.socket = "wss://stream.binance.com/ws/" + self.symbol.lower() + "@kline_" + self.period
        self.closes = self.getHistory('c')
        self.openFunc = partial(self.onOpen)
        self.closeFunc = partial(self.onClose)
        self.errorFunc = partial(self.onError)
        self.messageFunc = partial(self.onMessage)
        self.wsStream = websocket.WebSocketApp(self.socket,on_open=self.openFunc, on_close=self.closeFunc, on_error=self.errorFunc, on_message=self.messageFunc)

    def onOpen(self, ws):
        print("opened")
    
    def onClose(self, ws):
        print("Closed")
    
    def onError(self, ws, error):
        print(error)

    def onMessage(self, ws, message):
        jsonMessage = json.loads(message)
        #pprint.pprint(jsonMessage)
        candle = jsonMessage['k']
        isClosed = candle['x']
        close = candle['c']
        if(isClosed):
            self.closes.insert(0, float(close))
            # if self.getSignal() == 1 and self.inPosition == False: 
            #    print("guy")
            # elif self.getSignal() == -1 and self.inPosition == True:
            #     print("sell")
            self.getSignal()
            print("RSI:", self.getRSI(), ":", self.getRSISignal())

    def getSignal(self):
        for i in self.indicators:
            if i in ["ADX" , "ADXR", "CCI", "DX", "MFI", "MINUS_DI", "PLUS_DI", "STOCH", "STOCHF", "ULTOSC", "WILLR"]:
                function = getattr(talib, i)
                frame = getHistoricalData("klines", SYMBOL, PERIOD)
                result = function(frame['h'], frame['l'], frame['c'], 14)
            elif i in ["APO", "CMO", "MACD", "MACDEXT", "MACDFIX", "MOM", "PPO", "ROC", "ROCP", "ROCR", "ROCR100", "RSI", "STOCHRSI"]:
                function = getattr(talib, i)
                frame = getHistoricalData("klines", SYMBOL, PERIOD)
                result = function(frame['c'])
            elif i =="BOP":
                function = getattr(talib, i)
                frame = getHistoricalData("klines", SYMBOL, PERIOD)
                result = function(frame['o'], frame['h'], frame['l'], frame['c'], 14)
            print(i + ":" + result)
        return 0


    def run(self):
        self.wsStream.run_forever()

    def getRSISignal(self):
        rsi = self.getRSI()
        if rsi > 70:
            return "BEARISH"
        elif rsi < 30:
            return "BULLISH"
        else:
            return "HOLD"

    def getRSI(self):
        return talib.RSI(numpy.array(self.closes))[-1]

    def getHistory(self, column):
        values = []
        data = json.loads(requests.get(HTTP_ROOT + "klines" + '?symbol=' + self.symbol.upper() + '&interval=' + self.period).text)
        # print(data)
        df = pandas.DataFrame(data)
        df.columns = ['open_time',
            'o', 'h', 'l', 'c', 'v',
            'close_time', 'qav', 'num_trades',
            'taker_base_vol', 'taker_quote_vol', 'ignore']
        for i in df[column][-20:-1].tolist():
            values.append(float(i))
        return values[::-1]


blogan = Bot("btc", "usdt","1m", 10, ['RSI', 'ADX'])
blogan.run()

def getHistoricalData(data, symbol, interval):
    currentUrl= HTTP_ROOT + data + '?symbol=' + symbol + '&interval=' + interval
    data = json.loads(requests.get(currentUrl).text)

    df = pandas.DataFrame(data)
    df.columns = ['open_time',
                'o', 'h', 'l', 'c', 'v',
                'close_time', 'qav', 'num_trades',
                'taker_base_vol', 'taker_quote_vol', 'ignore']
    df.index = [datetime.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
    return df



def getADX():
    function = getattr(talib, "ADX")
    frame = getHistoricalData("klines", SYMBOL, PERIOD)
    result = function(frame['h'], frame['l'], frame['c'], 14)
    return result[-1]
    
def getADXR():
    function = getattr(talib, "ADXR")
    frame = getHistoricalData("klines", SYMBOL, PERIOD)
    result = function(frame['h'], frame['l'], frame['c'], 14)
    return result[-1]

def getDirectionalSignal():
    adx = getADX()
    adxr = getADXR()
    if adx > adxr:
        return BULLISH
    elif adx < adxr and adx > 25 and adxr > 25:
        return BEARISH
    else:
        return HOLD
        
# print("RSI:", getRSISignal())
# print("DIRECTION:", getDirectionalSignal())

def order(symbol, quantity, side):
    try:
        order = client.create_order(
            symbol=symbol,
            quantity=quantity,
            side=side,
            type=ORDER_TYPE_MARKET
            )
    except Exception as e:
        print(e)
        return False
    return True

#client = Client(cred.API_KEY, cred.SECRET_KEY)

#Places a buy order for 10 dollars

#order("BTCUSDT", 0.0002 , SIDE_BUY)

def plot(frame):
    fig = go.Figure(data=[go.Candlestick(x=frame['close_time'],
                    open=frame['o'],
                    high=frame['h'],
                    low=frame['l'],
                    close=frame['c'])])
    fig.show()
