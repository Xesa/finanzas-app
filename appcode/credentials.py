import base64
import nacl.utils
import nacl.public

from config import Constants
from appcode.crypto import Cipher

def _getBankCredentials():
    # TODO: no me gusta como se gestiona esto, investigar si es mejor hacerlo desde config.py
    # Returns the 'BANK_CREDENTIALS' property from the Secrets file or creates a new one
    bankCredentials = Constants.get('BANK_CREDENTIALS', "s")

    if (bankCredentials is None): return {}
    else: return bankCredentials

def encryptCredentials(args):

    # Gets the credentials
    bankCredentials = _getBankCredentials()

    # Encrypts the credentials
    credentials = {
        "user": Cipher.encryptElement(args['user']),
        "pass": Cipher.encryptElement(args['pass'])
    }

    # Sets the 'BANK_CREDENTIALS' property back to the secrets file
    try:
        bankCredentials[args["bank"]] = credentials
        Constants.write("BANK_CREDENTIALS", bankCredentials, "s")

    except Exception as err:
        print(err)
        return "Error: unexpected exception.", 400

    return "New credentials set.", 200

def decryptCredentials(bank):

    # Checks if the 'BANK_CREDENTIALS' property contains the specified bank
    bankCredentials = _getBankCredentials().get(bank)

    # Checks if the credentials exist
    if (bankCredentials is None or
        bankCredentials['user'] is None or
        bankCredentials['pass'] is None):
        return None

    # Decrypts the credentials
    try:
        decryptedCredentials = {
            "user" : Cipher.decryptElement(bankCredentials['user']),
            "pass" : Cipher.decryptElement(bankCredentials['pass'])
        }

        return decryptedCredentials

    except Exception as err:
        print(err)
        return None