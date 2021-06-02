#Testing suite 
import json
import sys
sys.path.insert(1, sys.path[0].replace("tests", "\\src", 1))
import controller as hue

#Hue test methods
def test_hue_get_request():
    """Tests that the json file is recieved and contains valid data"""
    response = hue.get_light_data()
    assert(not(response is None))
    string = json.dumps(response)
    assert("\"1\"" in string)

def test_hue_state_change():
    """Tests ability to turn hue light on/off"""
    response = hue.set_light_state(3, True)
    string = json.dumps(response.text)
    assert("success" in string)
    response = hue.set_light_state(3, False)
    string = json.dumps(response.text)
    assert("success" in string)

def test_hue_color_change():
    """
    Tests light ability to change color
    Note: Light must be turned on for test to work
    Note: Check for proper xy conversion was observed visually
    """
    #Checks color in xy space
    response = hue.set_light_color(hue , 3, (100,100,100))
    string = json.dumps(response.text)
    #Checks color outside of xy space
    assert("success" in string)
    response = hue.set_light_color(hue , 3, (255,0,0))
    string = json.dumps(response.text)
    assert("success" in string)

#test_hue_get_request()
#test_hue_state_change()
#test_hue_color_change()