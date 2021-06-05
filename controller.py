#File: controller.py
#Description: interface for controlling lights found on the phillips hue bridge

import requests
import json

#url to access hue bridge on local network
_base_url = "http://192.168.0.100/api/dQ8uv5kgFtCvVDdCUensB9HgujFEeXQyFb7M80Lu/lights"

def get_light_data():
    """Returns Json data for all lights."""
    data = requests.get(_base_url)
    json_file = json.loads(data.text)
    return json_file

def set_light_state(id, state):
    """
    Sends a put request to turn the light on or off

    Paramaters:
    id - Number id of a light to modify
    state - boolean to turn light on/off

    Returns:
    JSON response file
    """
    final_url = _base_url + "/" + str(id) + "/state"
    json_to_send = "{\"on\":" + str(state).lower() + "}"
    response = requests.put(final_url, json_to_send)
    return response;

def set_light_color(self, id, color):
    """
    Sends a put request given the data.

    Paramaters:
    id - Number id of a light to modify
    color - rgb tuple

    Returns:
    JSON response file
    """
    final_url = _base_url + "/" + str(id) + "/state"
    xy = self._calculate_xy_coordinates(color)
    xy = "[{},{}]".format(xy[0], xy[1])
    json_to_send = "{\"xy\":" + xy + "}"
    response = requests.put(final_url, json_to_send)
    return response;

def _calculate_xy_coordinates(color):
    """
    Helper method to calculate the xy color gamut point

    Paramaters:
    color - rgb tuple

    Returns:
    tuple formated(x,y)
    """
    #Converts rgb values to appropriate dec values
    for val in color:
        val = val / 255
        #Gamma Correction
        if(val > 0.04045):
            val = pow((val + .055) / 1.055, 2.4)
        else:
            val /= 12.92
    
    #Wide RGB D65 conversion
    X = color[0] * 0.649926 + color[1] * 0.103455 + color[2] * 0.197109
    Y = color[0] * 0.234327 + color[1] * 0.743075 + color[2] * 0.022598
    Z = color[0] * 0.000000 + color[1] * 0.053077 + color[2] * 1.035763

    #Convert to xy
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)

    #TODO: THIS CHUNK IS NOT CORRECT
    #Corrects xy if they are out of bounds
    if(x < .167):
        x = .167
    elif(x > .675):
        x = .675
    if(y < .04):
        y = .04
    elif(y > .518):
        y = .518
    
    return(x,y)