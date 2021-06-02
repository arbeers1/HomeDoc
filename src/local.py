#File: local.py
#Description: Responsible for retrieving weather, time, date

import requests
import datetime as datetime

#URl for getting temp, conditions
weather_url_city = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=1d5625b036b3668f000b321a50a3f82a&units=imperial"
#URL for getting hourly, weekly forecast
weather_url_call = "http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid=1d5625b036b3668f000b321a50a3f82a&units=imperial&exclude=minutely"

def date():
    """Return date formated 'Mon, June 01'"""
    current_time = datetime.now()
    return current_time.strftime("%a, %b %d") 

def time():
    """Return time formated 'hh:mm'"""
    current_time = datetime.now()
    hour = current_time.strftime("%I")
    hour = hour.lstrip("0")
    hour += ":" + current_time.strftime("%M")
    return hour

def next_days():
    """Return the days of the week such that today is at index 0 followed by the rest in order"""
    days_ordered = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
    day_index = int(datetime.now().strftime("%w"))
    days = [days_ordered[day_index]]
    for x in range(6):
        day_index += 1
        if(day_index > 6):
            day_index = 0
        days.append(days_ordered[day_index])
    return days

def temp_conditions(city):
    """
    Gets the current temperature and conditions at the given city

    Paramaters:
    city - the city to search

    Returns:
    tuple formated(temp, current conditions)
    """
    url = weather_url_city.format(city)
    result = requests.get(url)
    data = result.json()
    return(int(round(data["main"]["temp"])), data["weather"][0]["description"])

def lat_lon(city):
    """
    Gets the lattitude and longitude of a city

    Paramaters:
    city - the city to search

    Returns:
    tuple formatted(lat, lon)
    """
    url = weather_url_city.format(city)
    result = requests.get(url)
    data = result.json()
    return (data["coord"]["lat"], data["coord"]["lon"])

def weekly_forecast(lat, lon):
    """
    Returns 7 day forecast

    Paramaters: 
    lat - lattitude of area to search
    lon - longitude of area to search

    Returns
    list formatted(day1, day2, ...) where each day is (max_temp, min_temp, description)
    """
    url = weather_url_call.format(lat,lon)
    result = requests.get(url)
    data = result.json()
    list = data["daily"]
    final = []
    for x in range(7):
        daily_forecast = (int(round(list[x]["temp"]["max"])), int(round(list[x]["temp"]["min"])), list[x]["weather"][0]["description"])
        final.append(daily_forecast)
    print(final)

weekly_forecast(43.4711, -89.7443)
