from flask import Flask, render_template
from momentumIndicators import momentumIndicators
from currenciesAvailable import currenciesAvailable
from timePeriods import timePeriods

app = Flask(__name__)

@app.route("/")
def helloWorld():
    return render_template("home.html", momentumIndicators=momentumIndicators, currencies=currenciesAvailable, timePeriods=timePeriods)

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text