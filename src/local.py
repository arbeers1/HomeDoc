#File: local.py
#Description: Responsible for retrieving weather, time, date

import requests
from datetime import datetime

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
    tuple formated(temp, current conditions, min, max)
    """
    url = weather_url_city.format(city)
    result = requests.get(url)
    data = result.json()
    return(round(data["main"]["temp"]), data["weather"][0]["description"], round(data["main"]["temp_min"]), round(data["main"]["temp_max"]))

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
        daily_forecast = (str(round(list[x]["temp"]["max"])) + "??", str(round(list[x]["temp"]["min"])) + "??", list[x]["weather"][0]["description"])
        final.append(daily_forecast)
    return final

def hourly_forecast(lat, lon):
    """
    Returns hourly forecast for next 12 hours

    Paramaters:
    lat - lattitude of area to search
    lon - longitude of area to search

    Returns
    list formatted(hour1, hour2, ...) where each hour is (temp, conditions, hour)
    """
    url = weather_url_call.format(lat, lon)
    result = requests.get(url)
    data = result.json()
    list = data["hourly"]
    hours = hour_help()
    final = []
    for x in range(12):
        hourly_forecast = (str(round(list[x]["temp"])) + "??", list[x]["weather"][0]["description"], hours[x])
        final.append(hourly_forecast)
    return final

def hour_help():
    """
    Helper method which gets the next 12 hours formatted 'hPm/Am'

    Returns
    [hour1, hour2, ...] for a total of 12 hours.
    """
    hours = []
    current_time = datetime.now()
    time = current_time.strftime("%I")
    time = int(time)
    ending = current_time.strftime("%p")

    for x in range(12):
        if(time == 12 and ending == "AM"):
            ending = "PM"
        elif(time == 12):
            ending = "AM"

        if(time > 12):
            hours.append(str(time - 12) + ending)
        else:
            hours.append(str(time) + ending)
        time += 1
    hours[0] = "Now"
    return hours
