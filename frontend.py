from flask import Flask, render_template, request
from momentumIndicators import momentumIndicators
from currenciesAvailable import currenciesAvailable
from timePeriods import timePeriods
#from bot import Bot

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def helloWorld():
    print("++++")
    print("Coin One:", request.form.get("coinOne"))
    print("Coin Two:", request.form.get("coinTwo"))
    print("Period:", request.form.get("period"))
    vals = list(request.form.values())
    for i in range(3,len(vals), 3):
        print(vals[i] + ": buy: " + vals[i+1] + ", sell: " + vals[i+2])
    print("++++")
    return render_template("home.html", momentumIndicators=momentumIndicators, currencies=currenciesAvailable, timePeriods=timePeriods)
