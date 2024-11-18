import json
import os

class Constants:
    _data = None

    @classmethod
    def load(cls):

        if cls._data is None:
            with open('public-config.json', 'r') as file:
                try:
                    cls._data = json.load(file)
                except:
                    cls._data = {}

            with open('secrets.json', 'r') as file:
                try:
                    cls._data.update(json.load(file))
                except:
                    None

        return cls._data

    @classmethod
    def get(cls, key):
        return cls.load().get(key)

    @classmethod
    def write(cls, key, value, mode):
        if (key == "" or type(key) != str) : return None

        if (mode == "p"): fileName = "public-config.json"
        elif (mode == "s"): fileName = "secrets.json"
        else: return None

        with open(fileName, "r+") as file:
            data = json.load(file)
            data[key] = value
            file.seek(0)
            json.dump(data, file, indent=3)
            cls._data = data

        return cls._data