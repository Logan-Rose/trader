from flask import Flask, render_template, request
import json, pprint
from bot import Bot

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def autoQuant():

    with open('./info.json') as f:
        info = json.load(f)

    indicators = info['momentumIndicators']
    currencies = info['currenciesAvailable']
    periods = info['timePeriods']

    print("++++")
    coinOne = request.form.get("coinOne")
    print("Coin One:", coinOne)
    coinTwo = request.form.get("coinTwo")
    print("Coin Two:", coinTwo)
    period = request.form.get("period")
    print("Period:", period)
    amount = int(request.form.get("amount"))
    print("Amount:", amount)
    vals = list(request.form.values())[4:]

    for i in range(0, len(vals), 3):
        print("ind:", vals[i], ",buy:", vals[i+1], ",sell:",vals[i+2])

    return render_template("home.html", indicators=indicators, currencies=currencies, periods=periods)
