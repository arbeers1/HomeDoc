from flask import Flask, session, render_template, jsonify, request
from requests.api import get
from src.local import *
from src.controller import get_light_data, set_light_state, set_light_color, set_light_bri
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
    return render_template('index.html', vis = val, pointer = val2, time=time(), weather=str(temp) + "°")

@app.route("/invis")
def home_invis():
    return render_template('index.html', vis = 0, pointer = "auto", time=time(), weather=str(temp) + "°")

@app.route("/lights")
def lights():
    session["vis"] = 1
    return render_template('lights.html')

@app.route("/weather")
def weather():
    session["vis"] = 1
    tc = temp_conditions(config.city) #temp/conditions
    days = next_days() #next 7 days
    ll = lat_lon(config.city) #lat/lon (required for weekly forecast)
    week_f = weekly_forecast(ll[0], ll[1])
    hour_f = hourly_forecast(ll[0], ll[1])
    return render_template(
        'weather.html',
        date = date(), 
        temp = str(tc[0]) + "°", 
        min = str(tc[2]) + "°",
        max = str(tc[3]) + "°",
        conditions = tc[1].capitalize(), 
        city = config.city.capitalize(),
        d = days,
        wf = week_f,
        hf = hour_f
        )

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

@app.route('/update_lights', methods = ['GET', 'POST'])
def update_lights():
    if(request.method == 'GET'):
        return jsonify(main=get_light_data())
    if(request.method == 'POST'):
        if(request.form.get('state') == "true"):
            set_light_state(request.form.get('id'), request.form.get('state_val'))
        elif(request.form.get('color') == "true"):
            set_light_color(request.form.get('id'), request.form.get('color_val'))
        elif(request.form.get('bri') == "true"):
            set_light_bri(request.form.get('id'), request.form.get('bri_val'))
        return jsonify(result="None")