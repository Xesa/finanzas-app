from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import appcode.custom_webdriver as webdriver
from appcode.custom_webdriver import getElementByScript
from appcode.custom_webdriver import getElementBySelector
from appcode.custom_webdriver import sendKeys
from appcode.custom_webdriver import enterIFrame
from appcode.custom_webdriver import waitInterval

import time

import appcode.credentials
import appcode.file_scanner as fileScanner
import config

# In case anything fails here:
# The HTML elements are hidden in a Shadow DOM layer, the way they are configured
# may change overtime. Just change the identification strategy for the Shadow Hosts
# to find the elements that contain the Shadow Roots.

def _rejectCookies(driver):

    # Rejects cookies if prompted
    try:
        button_rejectCookies = getElementBySelector(driver, driver, By.ID, "onetrust-reject-all-handler")
        button_rejectCookies.click()
    except NoSuchElementException:
        pass

def _enterLoginPage(driver):

    # Gets the Shadow Root from the header element
    header = getElementBySelector(driver, driver, By.ID, 'no_customer')
    header_root = getElementByScript(driver, "return arguments[0].shadowRoot", header)

    # Gets the Shadow Root from the button container
    button_container = getElementBySelector(driver, header_root, By.CSS_SELECTOR, "bs-button.secondary.size-md.hydrated")
    button_container_root = getElementByScript(driver, "return arguments[0].shadowRoot", button_container)

    # Gets the login page button and clicks it
    login_button = getElementBySelector(driver, button_container_root, By.CSS_SELECTOR, 'button')

    login_button.click()

def _makeLogin(driver, credentials):

    # Gets the first Shadow Host, found by the ID 'login'
    bs_login = getElementBySelector(driver, driver, By.ID, 'login')

    # Jumps to the second Shadow Host, found by the tag name 'bs-form'
    bs_form = getElementByScript(driver, "return arguments[0].shadowRoot.querySelector('bs-form')", bs_login)

    # Retrieves the 'bs-input' elements for the username and password textboxes
    bs_username = getElementByScript(driver, "return arguments[0].querySelector('bs-input#username').querySelector('input')", bs_form)
    bs_password = getElementByScript(driver, "return arguments[0].querySelector('bs-input#password').querySelector('input')", bs_form)

    # Finally, retrieves the login button
    bs_button = getElementByScript(driver, "return arguments[0].querySelector('bs-button.submit')", bs_form)

    # Sends the credentials and presses the submit button
    sendKeys(bs_username, credentials.get('user'), Keys.TAB)
    sendKeys(bs_password, credentials.get('pass'), Keys.ENTER)
    bs_button.click()

def _downloadMovements(driver, credentials):

    # Enters the Account page
    account = getElementBySelector(driver, driver, By.XPATH, "//li//a[div//p[contains(text(), '5640')]]")
    account.click()

    # Enters the IFrame that contains the download form
    enterIFrame(driver, By.ID, "frameH5", By.XPATH, "/html/body/app-root/div/main/stencil-router/stencil-route-switch/stencil-route[2]/app-transactionslist-route-page/div/transactions-page/div/div[2]/div[1]/div[2]/div[2]/a")

    # Click on the download button to open the form
    download_button = getElementBySelector(driver, driver, By.XPATH, "/html/body/app-root/div/main/stencil-router/stencil-route-switch/stencil-route[2]/app-transactionslist-route-page/div/transactions-page/div/div[2]/div[1]/div[2]/div[2]/a")
    download_button.click()

    # Gets the elements from the download form
    download_form = getElementBySelector(driver, driver, By.TAG_NAME, "transactions-download-form")

    input_date_since = getElementBySelector(driver, download_form, By.XPATH, "/html/body/app-root/div/main/stencil-router/stencil-route-switch/stencil-route[2]/app-transactionslist-route-page/div/transactions-page/div/div[2]/div[1]/div[2]/div[2]/div/transactions-download-form/div/div/odp-form/div/div/div[1]/div/div/odp-range-date-picker/div/div[1]/odp-menu/div/div[1]/div/odp-date-picker/div/odp-input/div/div/input")
    input_date_to = getElementBySelector(driver, download_form, By.XPATH, "/html/body/app-root/div/main/stencil-router/stencil-route-switch/stencil-route[2]/app-transactionslist-route-page/div/transactions-page/div/div[2]/div[1]/div[2]/div[2]/div/transactions-download-form/div/div/odp-form/div/div/div[1]/div/div/odp-range-date-picker/div/div[2]/odp-menu/div/div[1]/div/odp-date-picker/div/odp-input/div/div/input")
    radio_txt = getElementBySelector(driver, download_form, By.ID, "transactions-download-form-format-txt")
    button_download = getElementBySelector(driver, download_form, By.ID, "transactions-download-form-send")

    # Sets the dates
    sendKeys(input_date_since, "01/11/2024", Keys.TAB)
    sendKeys(input_date_to, "24/11/2024", None)

    # Selects the TXT file type and clicks the download button
    waitInterval(0.1,0.3)
    radio_txt.click()

    waitInterval(0.05,0.15)
    button_download.click()
    time.sleep(3)

def _scanMovements():

    # Sets the headers and delimiter
    headers = ['fecha', 'concepto', 'fecha-efectiva', 'importe', 'saldo', 'algo', 'cuenta']
    delimiter = '|'

    movements = fileScanner.retrieveFileMovements(headers, delimiter)
    headersToFilter = ['fecha','concepto','importe']
    return fileScanner.filterFileMovements(movements, headersToFilter)

def getTransactions(args):

    # Instantiates the webdriver
    driver = webdriver.getChromeWithPrefs("https://www.bancsabadell.com/bsnacional/es/particulares/")

    # Rejects the cookies
    _rejectCookies(driver)
    waitInterval(0.1,0.3)

    # Enters the login page
    _enterLoginPage(driver)
    waitInterval(0.1, 0.3)

    # Retrieves the credentials from the secrets file and sends them to the login page
    credentials = appcode.credentials.decryptCredentials('Sabadell')
    _makeLogin(driver, credentials)

    # Downloads the movements and quits the driver
    _downloadMovements(driver, credentials)
    driver.quit()

    # Scans the file and returns the movements
    return _scanMovements()