#File: Configurator.py
#Description: Read/Write save file logic for user configurations
#Notes: File format is .csv structured:
#       _city,_theme,_background_type,_picture_index
#       where the default config is:
#       chicago,light,picture,0

import csv
import os

file = (os.path.dirname(os.path.abspath(__file__))).replace("src", "user_config.csv")

class configurator:

    def __init__(self):
        #Reads the save file, if no save file is found default attributes are set
        if(not(self.read_save())):
            self._city = "chicago"
            self._theme = "light"
            self._background_type = "picture"
            self._picture_index = 0

    def read_save(self):
        """
        Looks for and reads the file user_config.csv for user configuration data

        Returns:
        True if file was successfully read and values are updated
        False if file was not found, in such a case a default save file will 
            automatically be created and update the values accordingly
        """
        try:
            with open(file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                list = next(reader)
                self._city = list[0]
                self._theme = list[1]
                self._background_type = list[2]
                self._picture_index = int(list[3])
            return True
        except FileNotFoundError:
            self.write_save(False)
            return False

    def write_save(self, instance):
        """
        Writes configuration data to user_config.csv

        Paramaters:
        instance
            -True if save should be written with configurator instance vars
            -False if save should be written with default config, as described in file header

        Returns:
        True if operation was successful
        False if operation failed
        """
        try:
            with open(file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                if(instance):
                    writer.writerow([self._city, self._theme, self._background_type, self.picture_index])
                else:
                    writer.writerow(["chicago", "light", "picture", 0])
            return True
        except FileNotFoundError:
            return False

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city = city
 
    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, theme):
        self._theme = theme

    @property 
    def background_type(self):
        return self._background_type

    @background_type.setter
    def background_type(self, background_type):
        self._background_type = background_type

    @property
    def picture_index(self):
        return self._picture_index

    @picture_index.setter
    def picture_index(self, picture_index):
        self._picture_index = picture_index
