#File: controller.py
#Description: interface for controlling lights found on the phillips hue bridge

import requests
import json
import math

class Triangle():
    """
    Represents the color gamut triangle used by the philips hue light bulb.
    Useful for operations involving the xy triangle.
    """
    _x1 = .675
    _y1 = .322
    _x2 = .409
    _y2 = .518
    _x3 = .167
    _y3 = .04

    def in_bounds(self, x, y):
        """
        Returns if a point is within the hue gamut color triangle

        Paramaters:
        x - the x coord
        y - the y coord

        Returns:
        true if in triangle
        false otherwise
        """
        d1 = self._sign([x,y], [self._x1, self._y1], [self._x2, self._y2])
        d2 = self._sign([x,y], [self._x2, self._y2], [self._x3, self._y3])
        d3 = self._sign([x,y], [self._x3, self._y3], [self._x1, self._y1])

        neg = d1 < 0 or d2 < 0 or d3 < 0
        pos = d1 > 0 or d2 > 0 or d3 > 0

        return not(neg and pos)

    def _sign(self, p1, p2, p3):
        """
        Helper method to determine sign for in_bounds
        """
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    def getNearest(self, x, y):
        """
        Gets the nearest point on a triangle from the x,y coord

        Paramaters:
        x - the x coord
        y - the y coord

        Returns
        [x,y]
        """
        slope_bottom = (self._y1 - self._y3) / (self._x1 - self._x3)
        slope_left = (self._y2 - self._y3) / (self._x2 - self._x3)
        slope_right = (self._y1 - self._y2) / (self._x1 - self._x2)

        y_int1 = slope_bottom * -1 * self._x1 + self._y1
        y_int2 = slope_left * -1 * self._x2 + self._y2
        y_int3 = slope_right * -1 * self._x2 + self._y2

        slope1_inverse = -1 / slope_bottom
        slope2_inverse = -1 / slope_left
        slope3_inverse = -1 / slope_right

        #Find line containing inverse slope and x, y (perpendicular)
        #y - y1 = m(x - x1)
        y_inv1 = slope1_inverse * -1 * x + y
        y_inv2 = slope2_inverse * -1 * x + y
        y_inv3 = slope3_inverse * -1 * x + y

        # Finds where the regular line and inverse intersect
        # Mx + yint = INV(Mx) + yinv
        x = (y_inv1 - y_int1) / (slope_bottom - slope1_inverse)
        y = x * slope_bottom + y_int1
        xy1 = [x, y]
        x = (y_inv2 - y_int2) / (slope_left - slope2_inverse)
        y = x * slope_left + y_int2
        xy2 = [x, y]
        x = (y_inv3 - y_int3) / (slope_right - slope3_inverse)
        y = x * slope_right + y_int3
        xy3 = [x, y]

        xy = [x, y]
        #calculate distance
        d1 = math.dist(xy, xy1)
        d2 = math.dist(xy, xy2)
        d3 = math.dist(xy, xy3)

        if(d1 < d2 and d1 < d3):
            return xy1
        elif(d2 < d1 and d2 < d3):
            return xy2
        else:
            return xy3

#url to access hue bridge on local network
_base_url = "http://192.168.0.100/api/dQ8uv5kgFtCvVDdCUensB9HgujFEeXQyFb7M80Lu/lights"

def get_light_data():
    """
    Returns Json data for all lights.
    
    Returns:
    List formatted [(light1_id, light1_name, light1_on, [r,g,b], bri), (light2_...)]
    """
    data = requests.get(_base_url)
    js = json.loads(data.text)
    list = []
    for i in js:
        id = i
        name = js[i]["name"]
        on = js[i]["state"]["on"]
        rgb = xy_to_rgb(js[i]["state"]["xy"][0], js[i]["state"]["xy"][1], js[i]["state"]["bri"]) 
        bri = js[i]["state"]["bri"]
        list.append((id, name, on, rgb, bri))
    return list

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
    color - rgb list

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
    color - rgb list [r, g, b]

    Returns:
    list formated [x,y]
    """
    #Converts rgb values to appropriate dec values
    for i, val in enumerate(color):
        val = val / 255
        #Gamma Correction
        if(val > 0.04045):
            color[i] = pow((val + .055) / 1.055, 2.4)
        else:
            color[i] /= 12.92
    
    #Wide RGB D65 conversion
    X = color[0] * 0.649926 + color[1] * 0.103455 + color[2] * 0.197109
    Y = color[0] * 0.234327 + color[1] * 0.743075 + color[2] * 0.022598
    Z = color[0] * 0.000000 + color[1] * 0.053077 + color[2] * 1.035763

    #Convert to xy
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)

    #Corrects xy if they are out of bounds
    gamut = Triangle()
    if(gamut.in_bounds(x, y)):
        return [x, y]
    else:
        return gamut.getNearest(x, y)

def xy_to_rgb(x, y, bri):
    """
    Converts x,y to rgb for gui use

    Paramaters:
    x - the current x of the light
    y - the current y of the light
    bri - the current brightness of the light

    Returns:
    [r, g, b]
    """
    #Init vars
    z = 1 - x- y
    Y = bri / 255
    X = (Y/y) * x
    Z = (Y/y) * z

    #Wide RGB D65 conversion
    r =  X * 1.656492 - Y * 0.354851 - Z * 0.255038
    g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
    b =  X * 0.051713 - Y * 0.121364 + Z * 1.011530
    rgb = [r, g, b]
    #Reverse gamma correction
    for i, s in enumerate(rgb):
        if(s <= 0.0031308):
            s = 12.92 * s
        else:
            s = (1.0 + 0.055) * pow(s, (1.0 / 2.4)) - 0.055
        s = s * 255
        rgb[i] = math.trunc(s)
    
    return rgb
