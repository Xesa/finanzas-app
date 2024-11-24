import json

class Constants:
    _data = None

    @classmethod
    def load(cls):

        # If there is no data stored in the class, opens the config and secret files and reads them
        if cls._data is None:

            cls._data = {}

            # Opens the config file and reads the info
            with open('config-public.json', 'r') as file:
                try:
                    cls._data['public'] = json.load(file)
                except json.decoder.JSONDecodeError:
                    cls._data['public'] = {}

            # Opens the secrets file and reads the info
            with open('config-secrets.json', 'r') as file:
                try:
                    cls._data['secrets'] = (json.load(file))
                except json.decoder.JSONDecodeError:
                    cls._data['secrets'] = {}

        return cls._data

    @classmethod
    def get(cls, key, mode):

        # Checks if both the key and mode are empty and returns None if so
        if (key == "" or mode == ""):
            return None

        # Loads the data and returns it
        if (mode == "p"):
            return cls.load().get("public").get(key)
        elif (mode == "s"):
            return cls.load().get("secrets").get(key)
        else:
            return None

    @classmethod
    def write(cls, key, value, mode):

        # Checks if they key is empty or is not a valid string
        if (key == "" or type(key) != str) :
            return None

        # Checks which mode is selected and returns None if no mode is selected
        if (mode == "p"):
            fileName = "config-public.json"
            dict = "public"
        elif (mode == "s"):
            fileName = "config-secrets.json"
            dict = "secrets"
        else:
            return None

        # Opens the file and adds the updated key
        with open(fileName, "r+") as file:
            dictData = cls.load().get(dict)
            dictData[key] = value
            cls._data[dict] = dictData
            json.dump(dictData, file, indent=3)

        return cls._data