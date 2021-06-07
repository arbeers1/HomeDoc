#File: outlook.py
#Description: Handles api request to outlook email

from html.parser import HTMLParser
from json.decoder import JSONDecodeError
import requests
import webbrowser
import json
import os

class HTMLParse(HTMLParser):
        """
        A class to perform a simple parse on the HTML emails in Outlook
        """
        _final_string = ""

        def handle_data(self, data):
            self._final_string += data

        @property
        def result(self):
            self._final_string = self._final_string.replace("\r", "")
            self._final_string = self._final_string.replace("\n", "")
            return self._final_string

class outlook:
    """
    Read authenticated user emails
    """
    mail_url = "https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages"

    def __init__(self, auth):
        """
        Returns outlook which can be used to access user email.

        Paramaters:
        auth - an outlookAuth. Example constructor call: mail = outlook(auth = outlookAuth(secret))
        """
        self._auth = auth

    def get_mail(self, num, secret):
        """
        Retrieves user emails ordered by most recent date

        Paramaters:
        num - the number of emails to retrieve
        secret - The secret value obtained from microsoft devevloper account

        Returns:
        List formatted [(sender_name, sender_address, subject, preview, body), ...]
        """
        headers = {'Authorization': 'Bearer {0}'.format(self._auth.token)}
        payload = {'$top': num}
        result = requests.get(self.mail_url, params = payload, headers=headers)
        #Refreshes access token if request fails
        try:
            result.json()["error"]
            self._auth.refresh_token(secret)
            headers = {'Authorization': 'Bearer {0}'.format(self._auth.token)}
            result = requests.get(self.mail_url, params = payload, headers=headers)
        except KeyError:
            pass
        list = []
        for email in result.json()["value"]:
            sender_name = email["sender"]["emailAddress"]["name"]
            sender_address = email["sender"]["emailAddress"]["address"]
            subject = email["subject"]
            preview = email["bodyPreview"]
            preview = preview.replace("\r", "")
            preview = preview.replace("\n", "")
            message = email["body"]["content"]

            #Converts HTML email to a basic text format.
            #Note: It likely will not appear directly as the HTML may dictate
            parser = HTMLParse()
            parser.feed(message)
            message = parser.result

            list.append((sender_name, sender_address, subject, preview, message))
        return list 

class outlookAuth:
    """
    Authentications service for email use.
    Use to obtain authentication or refresh access.
    """
    _client_id = "2910022a-a03a-4f0d-ba3a-08c12977e896"
    _authorize_url = "https://login.microsoftonline.com/{}/oauth2/v2.0/authorize?client_id={}&response_type={}&redirect_uri={}&scope={}" 
    _token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    _scope = "mail.read%20offline_access"
    _file = (os.path.dirname(os.path.abspath(__file__))).replace("src", "cache_outlook.json")

    def __init__(self, secret):
        """
        Retrieves authorization from either the cache file or requests one if the file is not found.
        Stores authorization access in a file if it is not found.

        Paramaters:
        secret - The secret value obtained from microsoft devevloper account
        """
        try:
            with open(self._file, 'r') as js:
                data = json.load(js)
                self._access_token = data["access_token"]
        except (FileNotFoundError, JSONDecodeError):
            self._authorize_url = self._authorize_url.format("common", self._client_id, "code", "http://localhost", self._scope)
            webbrowser.open(self._authorize_url)
            code = input("Enter Url: ")
            code = code[code.index('=') + 1 : code.index('&')]
            payload = {
                       'client_id' : self._client_id, 
                       'code' : code, 
                       'redirect_uri' : 'http://localhost', 
                       'grant_type' : 'authorization_code', 
                       'client_secret' : secret
                      }
            result = requests.post(self._token_url, payload)
            self._access_token = result.json()["access_token"]
            with open(self._file, "w") as js:
                json.dump(result.json(), js, indent = 4)

    def refresh_token(self, secret):
        """
        Gets a new access token, saves, and returns it when the current access token is expired

        Paramaters:
        secret - The secret value obtained from microsoft devevloper account
        """
        with open(self._file, "r") as js:
            data = json.load(js)
            refresh_token = data["refresh_token"]

        payload = {
                    'client_id' : self._client_id, 
                    'scope' : "mail.read",
                    'redirect_uri' : 'http://localhost', 
                    'grant_type' : 'refresh_token',
                    'refresh_token' : refresh_token, 
                    'client_secret' : secret
                  }
        result = requests.post(self._token_url, payload)
        self._access_token = result.json()["access_token"]
        with open(self._file, "w") as js:
            json.dump(result.json(), js, indent = 4)
        return self._access_token

    @property
    def token(self):
        return self._access_token
