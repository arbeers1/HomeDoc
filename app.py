from flask import Flask, session
from flask import render_template
import random
import string

app = Flask(__name__)
letters = string.ascii_lowercase
app.secret_key = ''.join(random.choice(letters) for i in range(15))
 
@app.route("/")
def home():
    if(session.get("vis", None) == None):
        val = 0
        val2 = "auto"
    else:
        val = session.get("vis", None)
        val2 = "none"
    return render_template('index.html', vis = val, pointer = val2)

@app.route("/lights")
def lights():
    session["vis"] = 1
    return render_template('lights.html')

@app.route("/weather")
def weather():
    session["vis"] = 1
    return render_template('weather.html')