import websocket, json, pprint, binance, requests, pandas, datetime, talib
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import API_CREDENTIALS as cred
from binance.client import Client
from binance.enums import *

BULLISH = 1
HOLD = 0
BEARISH = -1

SOCKET = "wss://stream.binance.com/ws/"
HTTP_ROOT = 'https://api.binance.com/api/v1/'
SYMBOL = "BTCUSDT"
STREAM = "@kline_"
PERIOD = "1m"
URL =  SOCKET + SYMBOL + STREAM + PERIOD


def onOpen(ws):
    print("opened")

def onClose(ws):
    print("Closed")

def onError(ws, error):
    print(error)

def onMessage(ws, message):
    jsonMessage = json.loads(message)
    #pprint.pprint(jsonMessage)
    candle = jsonMessage['k']
    isClosed = candle['x']
    opened = candle['o']
    print("Close Price:", opened)

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

def getRSI():
    function = getattr(talib, "RSI")
    frame = getHistoricalData("klines", SYMBOL, PERIOD)
    result = function(frame['c'], 14)
    frame.to_csv("RSI")
    print(result[-1])
    return result[-1]

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

def getRSISignal():
    rsi = getRSI()
    if rsi > 70:
        return BEARISH
    elif rsi < 30:
        return BULLISH
    else:
        return HOLD

def getDirectionalSignal():
    adx = getADX()
    adxr = getADXR()
    if adx > adxr:
        return BULLISH
    elif adx < adxr and adx > 25 and adxr > 25:
        return BEARISH
    else:
        return HOLD
        
print("RSI:", getRSISignal())
print("DIRECTION:", getDirectionalSignal())

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
client = Client(cred.API_KEY, cred.SECRET_KEY)

#Places a buy order for 10 dollars

#order("BTCUSDT", 0.0002 , SIDE_BUY)




def plot(frame):
    fig = go.Figure(data=[go.Candlestick(x=frame['close_time'],
                    open=frame['o'],
                    high=frame['h'],
                    low=frame['l'],
                    close=frame['c'])])
    fig.show()


ws = websocket.WebSocketApp(URL,on_open=onOpen, on_close=onClose, on_error=onError, on_message=onMessage )
ws.run_forever()