import sys
sys.path.insert(1, sys.path[0].replace("tests", "\\src", 1))
import local as local

def test_lat_lon():
    result = local.lat_lon("baraboo")
    assert(result[0] == 43.4711 and result[1] == -89.7443)
    result = local.lat_lon("london")
    assert(result[0] == 51.5085 and result[1] == -.1257)

def test_temp_conditions():
    result = local.temp_conditions("baraboo")
    assert(result[0] > -200)
    assert(result[1] != None)

def test_weekly_forecast():
    result = local.weekly_forecast(43.4711, -89.7443)
    assert(result[0] != None)
    assert(result[0][0] > -200)
    assert(result[0][1] > -200)
    assert(result[0][2] != None)

def test_hourly_forecast():
    result = local.hourly_forecast(43.4711, -89.7443)
    assert(result[0] != None)
    assert(result[0][0] > -200)
    assert(result[0][1] != None)


#test_lat_lon()
#test_temp_conditions()
#test_weekly_forecast()
test_hourly_forecast()