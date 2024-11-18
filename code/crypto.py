from logging import Logger
import base64

from flask import request
from __main__ import app
from config import Constants
from nacl.public import PrivateKey, PublicKey, Box

def setSecretToken():
    privateKey = PrivateKey.generate()
    privateKey64 = base64.b64encode(privateKey.encode()).decode('utf-8')
    Constants.write("SECRET_TOKEN", privateKey64, "s")

@app.route("/set-credentials", methods=['GET'])
def encryptCredentials():

    try:

        # Get list of args
        args = {
            "bank" : request.args.get('bank'),
            "user" : request.args.get('user'),
            "pass" : request.args.get('pass')
        }

        # Check if any parameter is missing or blank
        if (args["bank"] is None or args["user"] is None or args["pass"] is None):
            return "Error: missing parameter.", 400

        if (args["bank"] == "" or args["user"] == "" or args["pass"] == ""):
            return "Error: parameters cannot be blank.", 400

        print("sttart")

        # Gets the secret token or creates a new one if it doesn't exist
        if (Constants.get('SECRET_TOKEN') is None):
            setSecretToken()

        secretToken = Constants.get('SECRET_TOKEN')

        print(secretToken)

        # Check if the secrets file has the 'BANK_CREDENTIALS' property and creates it if not
        bankCredentials = Constants.get('BANK_CREDENTIALS')

        if (bankCredentials is None):
            bankCredentials = {}

        print(bankCredentials)

        # Prepares the cipher
        privateKey = PrivateKey(base64.b64decode(secretToken))
        publicKey = privateKey.public_key

        cipher = Box(privateKey, publicKey)

        # Encodes the credentials
        userKey = base64.b64encode(cipher.encrypt(args["user"].encode())).decode('utf-8')
        passKey = base64.b64encode(cipher.encrypt(args["pass"].encode())).decode('utf-8')

        credentials = {
            "user" : userKey,
            "pass": passKey
        }

        # Sets the 'BANK_CREDENTIALS' property back to the secrets file
        bankCredentials[args["bank"]] = credentials

        print(bankCredentials)

        Constants.write("BANK_CREDENTIALS", bankCredentials, "s")

    except Exception as err:
        print(err)
        return "Error: unexpected exception.", 400

    return "New credentials set.", 200



