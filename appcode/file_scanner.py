from pathlib import Path
import csv
import json
import os

import config

def retrieveFileMovements(headers, delimiter):

    # Gets the filepath from the config file
    filepath = Path(config.Constants.get('file-path', 'p') + "\\downloads")

    # Lists all the files in the downloads path, if there is more than one returns an error
    txt_files = list(filepath.glob('*.txt'))

    if len(txt_files) > 1:
        return None

    # Opens the file and creates a json dict
    txt_file = txt_files[0]

    with open (txt_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=delimiter)
        data = []

        for row in reader:
            data.append(dict(zip(headers, row)))

    # Deletes the file and returns the json dict
    os.remove(txt_file)
    return data

def filterFileMovements(movements, headersToFilter):
    data = []
    for movement in movements:
        data.append({key: movement[key] for key in headersToFilter})

    return data