from flask import Flask, render_template
from momentumIndicators import momentumIndicators
app = Flask(__name__)

@app.route("/")
def helloWorld():
    return render_template("home.html", momentumIndicators=momentumIndicators)