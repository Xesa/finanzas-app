from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

import json
import time
import random
import os
import tempfile
from functools import reduce
from pathlib import Path

import appcode.credentials
import config

class ChromeWithPrefs(uc.Chrome):
    def __init__(self, *args, options=None, **kwargs):
        if options:
            self._handle_prefs(options)

        super().__init__(*args, options=options, **kwargs)

        # remove the user_data_dir when quitting
        self.keep_user_data_dir = False

    @staticmethod
    def _handle_prefs(options):
        if prefs := options.experimental_options.get("prefs"):
            # turn a (dotted key, value) into a proper nested dict
            def undot_key(key, value):
                if "." in key:
                    key, rest = key.split(".", 1)
                    value = undot_key(rest, value)
                return {key: value}

            # undot prefs dict keys
            undot_prefs = reduce(
                lambda d1, d2: {**d1, **d2},  # merge dicts
                (undot_key(key, value) for key, value in prefs.items()),
            )

            # create a user_data_dir and add its path to the options
            user_data_dir = os.path.normpath(tempfile.mkdtemp())
            options.add_argument(f"--user-data-dir={user_data_dir}")

            # create the preferences json file in its default directory
            default_dir = os.path.join(user_data_dir, "Default")
            os.mkdir(default_dir)

            prefs_file = os.path.join(default_dir, "Preferences")
            with open(prefs_file, encoding="latin1", mode="w") as f:
                json.dump(undot_prefs, f)

            # pylint: disable=protected-access
            # remove the experimental_options to avoid an error
            del options._experimental_options["prefs"]

def getDriver(url):

    # Creates the options for the Web Driver
    driverOptions = uc.ChromeOptions()
    #driverOptions.add_argument("--headless")
    driverOptions.add_argument("--disable-gpu")
    driverOptions.add_argument("--disable-images")
    driverOptions.add_argument("--start-maximized")
    driverOptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

    # Adds the download path in the preferences
    filepath = config.Constants.get('file-path', 'p') + "\\downloads"
    prefs = {"download.default_directory": filepath}

    driverOptions.add_experimental_option("prefs", prefs)

    # Initializes the driver
    driver = ChromeWithPrefs(options=driverOptions)
    driver.get(url)

    return driver

def getElementByScript(driver, script, container):
    return WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script(script, container))

def getElementBySelector(driver, container, selector, query):
    return WebDriverWait(driver, 10).until(
        lambda driver: container.find_element(selector, query))

def enterIFrame(driver, selector, query, selectorToBeLoaded, queryToBeLoaded):
    iframe =  WebDriverWait(driver, 10).until(
        lambda driver: driver.find_element(selector, query))

    driver.switch_to.frame(iframe)

    # Waits for the IFrame contents to be loaded
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((selectorToBeLoaded, queryToBeLoaded)))

def sendKeys(container, key, finalKey):
    for char in key:
        container.send_keys(char)
        waitInterval(0.05, 0.2)

    container.send_keys(finalKey) if finalKey is not None else None

def waitInterval(min, max):
    time.sleep(random.uniform(min, max))

def printElement(driver, element):
    print(driver.execute_script("return arguments[0].outerHTML", element))

def printElements(driver, container):
    for element in container:
        printElement(driver, element)

def helperFinder(driver):
    # In case anything fails, here are some extra methods to get the Shadow DOM elements

    # How to get any kind of element: shadow hosts, shadow roots, slots and nodes
    bs_layout = driver.find_element(By.XPATH, '/html/body/section[1]/bs-layout')
    bs_layout_root = driver.execute_script("return arguments[0].shadowRoot", bs_layout)
    bs_layout_slots = driver.execute_script("return arguments[0].shadowRoot.querySelectorAll('slot')", bs_layout)
    bs_layout_nodes = driver.execute_script("return arguments[0].assignedNodes()", bs_layout_slots)

    # Then you can print the element
    printElement(driver, bs_layout)

    # Or print all elements inside a container
    printElements(driver, bs_layout_slots)