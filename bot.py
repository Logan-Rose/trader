import websocket, json, pprint, binance, requests, pandas, datetime
from matplotlib import pyplot as plt

SOCKET = "wss://stream.binance.com/ws/"
HTTP_ROOT = 'https://api.binance.com/api/v1/'
SYMBOL = "BTCUSDT"
STREAM = "@kline_"
PERIOD = "1h"

url = SOCKET + SYMBOL + STREAM + PERIOD

file1 = open("text.txt", "w")

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

values = getHistoricalData("klines", SYMBOL, PERIOD)

prices = values['c'].astype('float')

plt.plot(prices)
plt.show()

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
    close = candle['c']

    if isClosed:
        print(close)

#ws = websocket.WebSocketApp(url,on_open=onOpen, on_close=onClose, on_error=onError, on_message=onMessage )
#ws.run_forever()
