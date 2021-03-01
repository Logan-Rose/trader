import websocket, json, pprint

SOCKET = "wss://stream.binance.com/ws/btcusdt@kline_1m"

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



ws = websocket.WebSocketApp(SOCKET,on_open=onOpen, on_close=onClose, on_error=onError, on_message=onMessage )
ws.run_forever()