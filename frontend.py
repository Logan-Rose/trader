from flask import Flask, render_template, request, redirect
import json, pprint
from bot import Bot

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

    data = {}
    print("++++")
    data['coinOne'] = request.form.get("coinOne")
    data['coinTwo'] = request.form.get("coinTwo")
    data['period'] = request.form.get("period")
    data['amount'] = request.form.get("amount")
    vals = list(request.form.values())[4:]
    for i in range(0, len(vals), 3):
        currentInd = {}
        currentInd['ind'] = vals[i]
        currentInd['buy'] = vals[i+1]
        currentInd['sell'] = vals[i+2]
        data[str(i)] = currentInd
    print()
    return render_template("terminal.html", data=json.dumps(data), indicators=indicators, currencies=currencies, periods=periods)
