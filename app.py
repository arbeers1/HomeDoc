from flask import Flask, session, render_template, jsonify, request
from src.local import temp_conditions
from src.configurator import configurator
import os

#Preload the user config and homescreen weather
config = configurator()
temp = temp_conditions(config.city)[0]

#Start application
app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
def home():
    if(session.get("vis", None) == None):
        val = 0
        val2 = "auto"
    else:
        val = session.get("vis", None)
        val2 = "none"
    return render_template('index.html', vis = val, pointer = val2, weather=str(temp) + "°")

@app.route("/lights")
def lights():
    session["vis"] = 1
    return render_template('lights.html')

@app.route("/weather")
def weather():
    session["vis"] = 1
    return render_template('weather.html')

@app.route("/email")
def email():
    session["vis"] = 1
    return render_template('email.html')

@app.route("/spotify")
def spotify():
    session["vis"] = 1
    return render_template('spotify.html')

@app.route('/update_home', methods = ['GET'])
def update():
    temp = temp_conditions(config.city)[0]
    return jsonify(weather=temp)