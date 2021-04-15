from flask import Flask, render_template, request, redirect
import json, pprint
from bot import Bot
import atexit

app = Flask(__name__)



@app.route("/", methods = ['GET', 'POST'])
def home():
    with open('./info.json') as f:
        info = json.load(f)
    indicators = info['momentumIndicators']
    currencies = info['currenciesAvailable']
    periods = info['timePeriods']
    return render_template("home.html", indicators=indicators, currencies=currencies, periods=periods)


@app.route("/run", methods = ['GET', 'POST'])
def autoQuant():

    with open('./info.json') as f:
        info = json.load(f)

    indicators = info['momentumIndicators']
    currencies = info['currenciesAvailable']
    periods = info['timePeriods']

    data = []
    print("++++")
    #data.append(request.form.get("coinOne"))
    #data.append(request.form.get("coinTwo"))
    #data.append(request.form.get("period"))
    #data.append(request.form.get("amount"))
    vals = list(request.form.values())[4:]
    for i in range(0, len(vals), 3):
        currentInd = []
        currentInd.append(vals[i])
        currentInd.append(int(vals[i+1]))
        currentInd.append(int(vals[i+2]))
        data.append(currentInd)
    print(data)
    trading = Bot(request.form.get("coinOne"), request.form.get("coinTwo"), request.form.get("period"), request.form.get("amount"), vals)
    trading.run()
    return render_template("terminal.html", data=data, indicators=indicators, currencies=currencies, periods=periods)
