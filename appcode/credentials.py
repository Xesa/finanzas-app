import base64

import nacl.utils
import nacl.public
from flask import request
from config import Constants
from flask import Blueprint
import appcode.crypto as crypto

credentials_bp = Blueprint('credentials', __name__, url_prefix='/credentials')

def getBankCredentials():
    # Returns the 'BANK_CREDENTIALS' property from the Secrets file or creates a new one

    bankCredentials = Constants.get('BANK_CREDENTIALS', "s")

    if (bankCredentials is None):
        return {}
    else:
        return bankCredentials

def encryptCredentials(args, bankCredentials, cipher):

    # Gets the credential bytes
    userBytes = args["user"].encode('utf-8')
    passBytes = args["pass"].encode('utf-8')

    # Encrypts the credential bytes
    nonce = nacl.utils.random(nacl.public.Box.NONCE_SIZE)

    userEncrypted = cipher.encrypt(userBytes, nonce)
    passEncrypted = cipher.encrypt(passBytes, nonce)

    # Converts the encrypted bytes into base64
    nonce64 = base64.b64encode(nonce).decode('utf-8')
    user64 = base64.b64encode(userEncrypted.ciphertext).decode('utf-8')
    pass64 = base64.b64encode(passEncrypted.ciphertext).decode('utf-8')

    credentials = {
        "nonce": nonce64,
        "user": user64,
        "pass": pass64
    }

    # Sets the 'BANK_CREDENTIALS' property back to the secrets file
    bankCredentials[args["bank"]] = credentials
    Constants.write("BANK_CREDENTIALS", bankCredentials, "s")

def decryptCredentials(bank):

    # Checks if the bank string is empty
    if (bank == "" or type(bank) != str):
        return None

    # Prepares the cipher
    secretToken = crypto.getSecretToken()
    cipher = crypto.getCipher(secretToken)

    # Checks if the 'BANK_CREDENTIALS' property contains the specified bank
    bankCredentials = getBankCredentials().get(bank)

    if (bankCredentials is None):
        return None

    # Gets the encrypted credentials
    nonceEncrypted = bankCredentials.get('nonce')
    userEncrypted = bankCredentials.get('user')
    passEncrypted = bankCredentials.get('pass')

    # Checks if the credentials exist
    if (nonceEncrypted is None or
            userEncrypted is None or
            passEncrypted is None):
        return None

    # Decodes the base64 credentials
    nonce64 = base64.b64decode(nonceEncrypted)
    user64 = base64.b64decode(userEncrypted)
    pass64 = base64.b64decode(passEncrypted)

    # Decrypts the credentials
    try:
        decryptedCredentials = {
            "user" : cipher.decrypt(user64, nonce64).decode('utf-8'),
            "pass" : cipher.decrypt(pass64, nonce64).decode('utf-8')
        }

        return decryptedCredentials

    except Exception as err:
        print(err)
        return None


@credentials_bp.route("/set-credentials", methods=['GET'])
def setCredentials():

    # TODO: algo falla al reemplazar una credencial, aparecen corchetes extra al final

    try:

        # Validates the access token
        if (crypto.validateToken(request.args.get('token')) is False):
            return "Forbidden", 403

        # Get list of args
        args = {
            "bank": request.args.get('bank'),
            "user": request.args.get('user'),
            "pass": request.args.get('pass')
        }

        # Check if any parameter is missing or blank
        if (args["bank"] is None or args["user"] is None or args["pass"] is None):
            return "Error: missing parameter.", 400

        if (args["bank"] == "" or args["user"] == "" or args["pass"] == ""):
            return "Error: parameters cannot be blank.", 400

        # Prepares the cipher
        secretToken = crypto.getSecretToken()
        cipher = crypto.getCipher(secretToken)

        # Encrypts the credentials
        bankCredentials = getBankCredentials()
        encryptCredentials(args, bankCredentials, cipher)

    except Exception as err:
        print(err)
        return "Error: unexpected exception.", 400

    return "New credentials set.", 200