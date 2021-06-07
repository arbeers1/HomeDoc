import sys
import os
sys.path.insert(1, sys.path[0].replace("tests", "\\src", 1))
from outlook import outlookAuth
from outlook import outlook
from configurator import configurator
config = configurator()

_file = (os.path.dirname(os.path.abspath(__file__))).replace("src", "cache_outlook.json")

def test_get_access_no_cache():
    #Tests retrieving a access code when no code is locally stored.
    #Make sure if a stored code exist, delete it
    auth = outlookAuth(config.outlook_secret)
    try:
        assert(auth.token != None)
        with open(_file, 'r') as file:
            return
    except AttributeError or FileNotFoundError:
        print("Failed test_get_access_no_cache")

def test_get_access_cache():
    #Ensure a cache_outlook.json is present in the HomeDoc directory
    auth = outlookAuth(config.outlook_secret)
    try:
        assert(auth.token != None)
    except AttributeError:
        print("Failed test_get_access_no_cache")

def test_refresh():
    auth = outlookAuth(config.outlook_secret)
    assert(auth.token != auth.refresh_token)

def test_get_emails():
    mail = outlook(outlookAuth(config.outlook_secret))
    list = mail.get_mail(1, config.outlook_secret)
    for i in list:
        print(i)

#test_get_access_no_cache()
#test_get_access_cache()
#test_refresh()
test_get_emails()