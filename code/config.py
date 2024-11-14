import json

class Constants:
    _data = None

    @classmethod
    def load(cls):

        if cls._data is None:
            with open('../public-config.json', 'r') as file:
                cls._data = json.load(file)

            with open('../secrets.json', 'r') as file:
                cls._data.update(json.load(file))

        return cls._data

    @classmethod
    def get(cls, key):
        return cls.load().get(key)