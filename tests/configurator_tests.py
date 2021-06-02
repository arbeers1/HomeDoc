import sys
import os
import csv
sys.path.insert(1, sys.path[0].replace("tests", "\\src", 1))
from configurator import configurator

file = (os.path.dirname(os.path.abspath(__file__))).replace("tests", "user_config.csv")

#Note: for this test to work a correctly formatted csv with the following attributes must be present
def test_read_save():
    config = configurator()
    assert(config.city == "new york")
    assert(config.theme == "dark")
    assert(config.background_type == "picture")
    assert(config.picture_index == 0)

#Note: for this test to work no user_config.csv file should be present in the HomeDoc directory
def test_read_save_no_file():
    config = configurator()
    assert(config.city == "chicago")
    assert(config.theme == "light")
    assert(config.background_type == "picture")
    assert(config.picture_index == 0)

def test_write_save_instance():
    config = configurator()
    config.city = "test1"
    config.theme = "future"
    config.background_type = "color"
    config.picture_index = -1
    assert(config.write_save(True))
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        list = next(reader)
        assert(list[0] == "test1")
        assert(list[1] == "future")
        assert(list[2] == "color")
        assert(int(list[3]) == -1)

def test_write_save_default():
    config = configurator()
    config.city = "False Value"
    assert(config.write_save(False))
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        list = next(reader)
        assert(list[0] == "chicago")


#test_read_save()
#test_read_save_no_file()
#test_write_save_instance()
test_write_save_default()