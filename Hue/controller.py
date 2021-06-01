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
    state - 'true' or 'false' to turn light on/offf
    """
    #TODO: Finish method

def set_light_color(id, hue, sat, bri):
    """
    Sends a put request given the data.

    Paramaters:
    id - Number id of a light to modify
    hue -  Value of hue between 0 and 65535 or None
    sat - Value of sat between 0 and 254 or None
    bri - Value of bri between 1 and 254 or None
    """
    final_url = _base_url + "/" + id + "/state"
    #TODO: Finish method