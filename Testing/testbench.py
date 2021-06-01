#Testing suite 
import json
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from Hue import controller as hue

#Hue test methods
def _test_hue_get_request():
    """Tests that the json file is recieved and contains valid data"""
    file = hue.get_light_data()
    assert(not(file is None))
    string = json.dumps(file)
    assert("\"1\" in string")

#_test_hue_get_request()
