from flask import Flask, render_template, request
import json, pprint
#from bot import Bot

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def autoQuant():

    with open('./info.json') as f:
        info = json.load(f)

    indicators = info['momentumIndicators']
    currencies = info['currenciesAvailable']
    periods = info['timePeriods']

    print("++++")
    print("Coin One:", request.form.get("coinOne"))
    print("Coin Two:", request.form.get("coinTwo"))
    print("Period:", request.form.get("period"))

    vals = list(request.form.values())
    for i in range(3,len(vals), 3):
        print(vals[i] + ": buy: " + vals[i+1] + ", sell: " + vals[i+2])
    print("++++")
    return render_template("home.html", indicators=indicators, currencies=currencies, periods=periods)
